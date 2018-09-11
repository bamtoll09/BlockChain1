def asdf(i):
    ass = i + 1
    while not (ass % 9 == 0 and ass % i == 0):
        ass += 1

    return ass

print asdf(6)
