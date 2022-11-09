from datetime import datetime
from pprint import pprint
from time import gmtime, mktime

from dateutil import tz

# import yfinance as yf
"""
    *************************************************
    인플레이션:    채권 down       원자재 up         주식 down
    스태그플레이션: 채권 up         원자재 down        주식 down
    리세션:       채권 up         원자재 down       주식 up
    골디락스:      채권 down       원자재 up         주식 up
    *************************************************
"""

from econcycle.utils.chart import Chart


class Cycle:
    def __init__(self, resolution, period, start_date, end_date):
        self._c = Chart(resolution, period, start_date, end_date)

        self.bond = self._c.process("AGG")
        self.raw_material = self._c.process("DBC")
        self.stock = self._c.process("SPY")

    def is_interest_rate_up(self, index: int) -> bool:
        # return a.get("type") == "downtrend" and s.get("type") == "downtrend"
        return (
            self.bond[index].get("type") == "downtrend"
            and self.stock[index].get("type") == "downtrend"
        )

    def is_inflation_up(self, index: int) -> bool:
        # return d.get("type") == "uptrend" and d.get("RSI") > 50.0
        return (
            self.raw_material[index].get("type") == "uptrend"
            and self.raw_material[index].get("RSI") > 50.0
        )

    def is_economy_good(self, index: int) -> bool:
        # return d.get("RSI") > 50.0 or s.get("RSI") > 50.0
        return (
            self.raw_material[index].get("RSI") > 50.0
            or self.stock[index].get("RSI") > 50.0
        )

    def is_inflation(self, index: int) -> bool:
        # return (
        #     self.is_economy_good(d, s)
        #     and self.is_inflation_up(d)
        #     and self.is_interest_rate_up(a, s)
        #     and a.get("RSI") < 50.0
        #     and d.get("RSI") > 65.0
        #     and s.get("RSI") < 50.0
        # )
        return (
            self.is_economy_good(index)
            and self.is_inflation_up(index)
            and self.is_interest_rate_up(index)
            and self.bond[index].get("RSI") < 50.0
            and self.raw_material[index].get("RSI") > 65.0
            and self.stock[index].get("RSI") < 50.0
        )

    def is_recession(self, index: int) -> bool:
        return (
            not (self.is_economy_good(index))
            and not (self.is_inflation_up(index))
            and not (self.is_interest_rate_up(index))
        )

    def is_stagflation(self, index: int) -> bool:
        return (
            not (self.is_economy_good(index))
            and self.is_inflation_up(index)
            and self.is_interest_rate_up(index)
        )

    def is_goldilocks(self, index: int) -> bool:
        return (
            self.is_economy_good(index)
            and not (self.is_inflation_up(index))
            and not (self.is_interest_rate_up(index))
        )

    def get_all(self):
        ret = []

        for i in range(len(self.bond)):
            data = {
                "Date": self.bond[i].get("Date"),
                "Bond_rsi": self.bond[i].get("RSI"),
                "Raw_material_rsi": self.raw_material[i].get("RSI"),
                "Stock_rsi": self.stock[i].get("RSI"),
            }
            if self.is_recession(i):
                data["Type"] = "Recession"
            elif self.is_inflation(i):
                data["Type"] = "Inflation"
            elif self.is_goldilocks(i):
                data["Type"] = "Goldilocks"
            # elif self.is_stagflation(i):
            #     data["Type"] = "Stagflation"
            else:
                data["Type"] = "Undefined"
            ret.append(data)
        return ret
