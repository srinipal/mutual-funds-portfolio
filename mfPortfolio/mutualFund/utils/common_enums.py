from enum import Enum

class AssetClass(Enum):
    EQUITY = "Equity"
    DEBT = "Debt"
    OTHERS = "Others"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]