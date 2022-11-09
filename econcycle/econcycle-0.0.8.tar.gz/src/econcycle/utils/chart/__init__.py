from datetime import datetime
from time import gmtime, mktime

import finnhub


class Chart:
    def __init__(self, resolution, period, start_date, end_date):
        self.f = finnhub.Client(
            api_key="cdfl83iad3i8a4q95080cdfl83iad3i8a4q9508g"
        )

        self.resolution = resolution
        self.period = period

        self.start_date = start_date
        self.end_date = end_date

        self.start_timestamp = self.to_timestamp(self.start_date)
        self.end_timestamp = self.to_timestamp(self.end_date)

    def to_timestamp(self, date: str) -> int:
        return int(
            datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
        )

    def calc_chart_frame(self, dx):
        cnt = 0
        arr_calc = []
        arr_candle = []
        dataxxx = []
        for i in range(len(dx["o"])):
            arr_calc.append({})
            arr_candle.append(
                {
                    "Open": float(dx.get("o")[i]),
                    "High": float(dx.get("h")[i]),
                    "Low": float(dx.get("l")[i]),
                    "Close": float(dx.get("c")[i]),
                }
            )
            my_data = {
                "Date": datetime.fromtimestamp(
                    mktime(gmtime(dx.get("t")[i]))
                ).strftime("%Y-%m-%d %H:%M:%S"),
                "Time": dx.get("t")[i],
                # "Volume": float(dx_data.get("volume")),
                "HighestPoint": {},
                "LowestPoint": {},
                "Candle": arr_candle[cnt],
                "i": cnt,
                "calculations": arr_calc[cnt],
            }
            if dx.get("rsi") != None:
                my_data["RSI"] = dx.get("rsi")[i]
            dataxxx.append(my_data)
            cnt = cnt + 1

        return dataxxx

    def highest_bars(self, result, period, index, lastPrice):
        if index > period:  # 20, 40
            for i in range(index - period, index + 1):
                if result[i].get("Candle").get("High") > lastPrice:
                    lastPrice = result[i].get("Candle").get("High")
                    result[i]["HighestPoint"] = {
                        "type": "highest",
                        "value": result[i].get("Candle").get("High"),
                        "date": result[i].get("Date"),
                        "time": result[i].get("Time"),
                    }

    def lowest_bars(self, result, period, index, lastPrice):
        if index > period:
            for i in range(index - period, index + 1):
                if result[i].get("Candle").get("Low") < lastPrice:
                    lastPrice = result[i].get("Candle").get("Low")
                    result[i]["LowestPoint"] = {
                        "type": "lowest",
                        "value": result[i].get("Candle").get("Low"),
                        "date": result[i].get("Date"),
                        "time": result[i].get("Time"),
                    }

    def draw_trend_line(self, data: list, period: int):
        myArray = []
        for i in range(len(data)):
            if i > period:
                self.highest_bars(data, period, i, 0)
                self.lowest_bars(data, period, i, 1000000000)
                if len(data[i].get("HighestPoint")) > 0:
                    myArray.append(data[i].get("HighestPoint"))
                if len(data[i].get("LowestPoint")) > 0:
                    myArray.append(data[i].get("LowestPoint"))

        dos = sorted(myArray, key=lambda x: x["time"])

        uptrend = []
        downtrend = []

        for s in range(len(dos)):
            if s < 2:
                continue
            if (
                dos[s - 1].get("type") == "lowest"
                and dos[s].get("type") == "highest"
            ):
                # print("UP")
                # pprint(dos[s - 1])
                # pprint(dos[s])
                uptrend.append(dos[s - 1])
            elif (
                dos[s - 1].get("type") == "highest"
                and dos[s].get("type") == "lowest"
            ):
                # print("DOWN")
                # pprint(dos[s - 1])
                # pprint(dos[s])
                downtrend.append(dos[s - 1])
        trend = uptrend + downtrend

        return sorted(trend, key=lambda k: k["time"])

    def set_trend(self, data: list, trend: list):
        i = 0
        if len(trend) > 1:
            for d in data:
                if d.get("Time") >= trend[i].get("time") and d.get(
                    "Time"
                ) < trend[i + 1].get("time"):
                    if trend[i].get("type") == "lowest":
                        d["type"] = "uptrend"
                    elif trend[i].get("type") == "highest":
                        d["type"] = "downtrend"
                    else:
                        raise Exception("Trend is not set correctly.")
                elif d.get("Time") >= trend[i + 1].get("time"):
                    if trend[i + 1].get("type") == "lowest":
                        d["type"] = "uptrend"
                    elif trend[i + 1].get("type") == "highest":
                        d["type"] = "downtrend"
                    else:
                        raise Exception("Trend is not set correctly.")
                    i += 1 if i + 2 < len(trend) else 0
                else:
                    d["type"] = "undefined"
                del d["HighestPoint"]
                del d["LowestPoint"]
                # pprint(d)
        else:
            for d in data:
                if d.get("Time") >= trend[i].get("time"):
                    if trend[i].get("type") == "lowest":
                        d["type"] = "uptrend"
                    elif trend[i].get("type") == "highest":
                        d["type"] = "downtrend"
                    else:
                        raise Exception("Trend is not set correctly.")
                else:
                    d["type"] = "undefined"
                del d["HighestPoint"]
                del d["LowestPoint"]

    def process(self, symbol: str) -> list:
        res = self.f.technical_indicator(
            symbol=symbol,
            resolution=self.resolution,
            _from=self.start_timestamp,
            to=self.end_timestamp,
            indicator="rsi",
            indicator_fields={"timeperiod": 14},
        )

        results = self.calc_chart_frame(res)

        trend = self.draw_trend_line(results, self.period)
        self.set_trend(results, trend)

        return results
