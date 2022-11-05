def isTriangle(a, b, c):  # 判断是否为三角形
    shortest = min(a, b, c)
    longest = max(a, b, c)
    middle = sum([a, b, c]) - shortest - longest
    if shortest <= 0 or (shortest + middle) <= longest:
        print('NO')
    elif shortest ** 2 + middle ** 2 == longest ** 2:
        print('YES')
    else:
        print('NO')
