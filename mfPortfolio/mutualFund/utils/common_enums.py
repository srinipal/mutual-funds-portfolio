from enum import Enum

class AssetClass(Enum):
    EQUITY = "Equity"
    DEBT = "Debt"
    OTHERS = "Others"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class MutualFundType(Enum):
    MULTI_CAP = 'Multi Cap Fund'
    MID_CAP = 'Mid Cap Fund'
    DIV_YIELD = 'Dividend Yield Fund'
    FOCUSED_FUND = 'Focused Fund'
    LARGE_CAP = 'Large Cap Fund'
    SMALL_CAP = 'Small Cap Fund'
    THEMATIC_FUND = 'Thematic Fund'
    VALUE_FUND = 'Value Fund'
    LARGE_MID_CAP = 'Large & Mid Cap Fund'
    ELSS = 'ELSS'
    CONTRA_FUND = 'Contra Fund'

    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]


    def display(self):
        return self.value