from dataclasses import dataclass
from datetime import date

@dataclass
class Ope:
    date: date
    lib: str
    montant: float

    DATE_EOF = date(9999, 12, 31)

    def __str__(self):
        return f"[{self.date.strftime('%d/%m/%Y')} / {self.lib[:50]:<50} / {self.montant}]"

    def isEOF(self):
        return self.date == Ope.DATE_EOF

    @staticmethod
    def EOF():
        return Ope(Ope.DATE_EOF, '', 0)
