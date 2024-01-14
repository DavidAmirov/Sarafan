def sequence(n):
    res = []
    for i in range(1, n+1):
        for k in range(i):
            if len(res) >= n:
                break
            else:
                res.append(str(i))
    return ''.join(res)


def sequence2(n):
    res = ''
    for i  in range(1, n+1):
        if len(res) <= n:
            res += str(i) * i
    return res[:n]


if __name__=='__main__':
    n = int(input('Введите длину последовательности: '))
    print(sequence(n))
    print(sequence2(n))