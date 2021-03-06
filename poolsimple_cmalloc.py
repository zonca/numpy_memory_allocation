import gc

import sys
import traceback

import time
import numpy as np

def create_arrays(div, ndata):
    dlist = []
    for d in range(div):
        dlist.append(np.ones(ndata, dtype=np.float64))
    print("  done with allocation", flush=True)
    time.sleep(5)

def main():
    datasize = 5000000000 # ~40GB
    mindiv = 4096 # 1 array of ~40GB
    maxdiv = 4096*4 # 65536 arrays of ~610KB

    div = mindiv
    while div <= maxdiv:
        ndata = datasize // div
        asize = ndata * 8
        asize_mb = asize / 1000000.0

        print("Testing {} arrays size of {:2.2f} MB".format(div, asize_mb),
            flush=True)

        create_arrays(div, ndata)
        print("  Arrays freed", flush=True)

        time.sleep(5)

        div *= 2

    print("Allocate with malloc now", flush=True)
    from cython_malloc import create_array_malloc
    create_array_malloc(datasize)

    time.sleep(10)

if __name__ == "__main__":
    try:
        main()
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print("".join(lines), flush=True)
