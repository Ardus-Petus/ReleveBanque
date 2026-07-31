# extraction_metier.py
from decimal import Decimal
import locale
from typing import Type
from ReleveBanque.core.Excel import Excel
from ReleveBanque.core.HTML import HTML

class ManqueHistorique(Exception):
    pass

class ExtractionMetier:
    def __init__(self, mod_XL:Type[Excel], mod_HTML:Type[HTML], tabexcl):
        self.mod_XL = mod_XL
        self.mod_HTML = mod_HTML
        self.tabexcl = tabexcl
        self.oHTML = None
        self.oXL = None

    def run(self, callback=None):
        def _cb(msgtype, value):
            if callback:
                callback(msgtype, value)
        def _tr(msg):
            _cb("log", msg+'\n')
        def _trace_ope(ope, inc_excl='incluse'):
            _cb(
                    "row",
                    (
                        inc_excl,
                        ope.date.strftime("%d/%m/%Y"),
                        ope.lib,
                        locale.currency(ope.montant, grouping=True, symbol=True),
                    ),
                )

            
        # Ouverture HTML
        self.oHTML = self.mod_HTML()

        # Signaler au GUI que HTML est ouvert (pour positionnement fenêtre)
        _cb("html_opened", self.oHTML.proc.pid)
        _cb("HTML", self.oHTML) # Pour communiquer l'objet

        # Attente connexion + relevé
        _tr("Attente de la connexion au site...")
        self.oHTML.waitForCnxComptes()

        _tr("Attente du choix du compte...")
        self.oHTML.waitForRelevé()

        acctNo = self.oHTML.getAcctNo()
        _cb("N° compte", acctNo)

        # Ouverture Excel
        _tr("Ouverture classeur Excel")
        oXL = self.mod_XL(acctNo)
        _cb("XL_opened", oXL)   # pour que l’UI positionne la fenêtre Excel
        _cb("XL", oXL)  # Pour communiquer l'objet
        _cb("Excel", oXL.getStatusString())
    
        # Recherche dernière opération Excel
        lastrow = oXL.getLastRow()
        try:
            lastope = oXL.getXLOpe(lastrow)
        except:
            raise ValueError("La dernière ligne du tableau Excel n\'est pas une écriture")
        _tr(f"Dern. opé: {lastope}")
        _cb("Dern. ", lastope)

        idxHTML = 0
        tot_excl = Decimal(0)

        # Ignorer les opérations exclues
        while True:
            ope = self.oHTML.getHTMLOpe(idxHTML)
            if ope.lib in self.tabexcl:
                _trace_ope(ope, "exclue ")
                tot_excl += Decimal(ope.montant)
                idxHTML += 1
            else:
                break

        # Empiler les opérations HTML jusqu’à lastope ou EOF
        operations = []
        while not (ope == lastope or ope.isEOF()):
            _trace_ope(ope)
            operations.append(ope)
            idxHTML += 1
            ope = self.oHTML.getHTMLOpe(idxHTML)

        nb_ope = len(operations)
        _cb("Nb ope", nb_ope)

        soldeHTML = Decimal(self.oHTML.getSolde())
        self.oHTML.quit()

        # Vérifier l’historique
        if oXL.status != oXL.NEW and ope.isEOF():
            raise ManqueHistorique(
                "Le relevé HTML ne contient pas assez d'historique pour remplir le fichier Excel."
            )

        # Dépiler vers Excel
        row = lastrow + 1
        tot_ope = Decimal(0)
        while operations:
            ope = operations.pop()
            oXL.StoreOpe(ope)
            tot_ope += Decimal(ope.montant)
            row += 1

        # Solde initial + sauvegarde
        if nb_ope:
            if oXL.status == oXL.NEW:
                oXL.solde_initial = soldeHTML - tot_ope - tot_excl
            oXL.saveWB()

        _cb(
                "log",
                f"Solde: {locale.currency(soldeHTML, grouping=True, symbol=True)}\n"
                f"Résultat: {nb_ope} opération(s) ajoutée(s)\n"
            )
        _tr("Fin normale du programme")
        _cb("fnorm", None)

        return True
