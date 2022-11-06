import re

pattern = re.compile(r'(?<!^)(?=[A-Z])')


def to_underline(value):
    if isinstance(value, str):
        value = pattern.sub('_', value).lower()
    elif isinstance(value, dict):
        new_value = {}
        for item in value.keys():
            new_value[to_underline(item)] = value[item]
        value = new_value
    return value


if __name__ == '__main__':
    v = to_underline("HelloWorld")
    print(v)
    v = to_underline({
        "orderViewId": "900233943035644687",
        "orderAmount": "19.00",
        "orderPayTime": 1665371274,
        "payEstimateBonus": "0.57",
        "settleEstimateBonus": "0.57",
        "tenant": 1
    })
    print(v)
