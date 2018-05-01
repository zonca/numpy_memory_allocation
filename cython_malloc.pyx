import random
from libc.stdlib cimport malloc, free

def create_array_malloc(long number=1):
    # allocate number * sizeof(double) bytes of memory
    cdef double *my_array = <double *>malloc(number * sizeof(double))
    cdef long i
    for i in range(number):
        my_array[i] = 0.
    if not my_array:
        raise MemoryError()
