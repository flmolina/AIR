cpdef int test(int x):
    cdef int i
    for i in range(x):
        i+=1
    return i