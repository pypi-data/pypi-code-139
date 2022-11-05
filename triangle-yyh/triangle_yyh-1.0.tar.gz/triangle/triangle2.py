def area(a, b, c):  # 判断三角形并返回面积
    shortest = min(a, b, c)
    longest = max(a, b, c)
    middle = sum([a, b, c]) - shortest - longest
    if shortest <= 0 or (shortest + middle) <= longest:
        print('NO')
    elif shortest ** 2 + middle ** 2 == longest ** 2:
        p = (a + b + c) / 2
        area = (p * (p - a) * (p - b) * (p - c)) ** (1/2)
        print('YES')
        return area
    else:
        print('NO')
