def sumValues(a, b, *others):
    retValue = a + b

    # Tham số 'others' giống như một mảng.
    for other in others:
        retValue = retValue + other

    return retValue