
def test():
    b = 0.0000000000000003
    a = 10.000
    for i in range(10):
        try:
            a = a / b
        except ZeroDivisionError:
            print('yeah')
            a = 5.0 * 1e99
    return a


print(test())