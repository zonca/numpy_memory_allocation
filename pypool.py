from mpi4py import MPI

import sys
import traceback

import time
import numpy as np


def main():
    datasize = 5000000000 # ~40GB
    mindiv = 1024 # 1 array of ~40GB
    maxdiv = 1024*16 # 65536 arrays of ~610KB

    rank = MPI.COMM_WORLD.rank
    nproc = MPI.COMM_WORLD.size

    div = mindiv
    while div < maxdiv:
        ndata = datasize // div
        asize = ndata * 8
        asize_mb = asize / 1000000.0

        if rank == 0:
            print("Testing {} arrays size of {:2.2f} MB".format(div, asize_mb),
                flush=True)

        for p in range(nproc):
            # Take turns allocating and freeing
            if rank == p:
                dlist = []
                for d in range(div):
                    dlist.append(np.ones(ndata, dtype=np.float64))
                print("  Proc {} done with allocation".format(p), flush=True)
                del dlist
                print("  Proc {} freed".format(p), flush=True)
            MPI.COMM_WORLD.barrier()

        time.sleep(10)
        MPI.COMM_WORLD.barrier()
        if rank == 0:
            print("  All procs done",
                flush=True)

        div *= 2

    return


if __name__ == "__main__":
    try:
        main()
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        lines = [ "Proc {}: {}".format(MPI.COMM_WORLD.rank, x) for x in lines ]
        print("".join(lines), flush=True)
        MPI.COMM_WORLD.Abort()
