import random
from libc.stdlib cimport malloc, free

def create_array_malloc(long number=1):
    # allocate number * sizeof(double) bytes of memory
    cdef double *my_array = <double *>malloc(number * sizeof(double))
    if not my_array:
        raise MemoryError()
