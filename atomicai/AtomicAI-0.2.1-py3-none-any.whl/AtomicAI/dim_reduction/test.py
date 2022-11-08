j = [1, 2, 4, 6, 7, 8]
for i in range(0, 10):
    try:
        if i in j:
            print(i)
    except:
        print(f'{i} is not here')
        break 
    print(i, j)
