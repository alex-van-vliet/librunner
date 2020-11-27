from mpi4py import MPI


class Process:
    comm_: MPI.Intracomm
    rank_: int
    size_: int

    def __init__(self, comm=None):
        self.comm_ = comm if comm is not None else MPI.COMM_WORLD
        self.rank_ = self.comm_.Get_rank()
        self.size_ = self.comm_.Get_size()

    def size(self):
        return self.size_

    def rank(self):
        return self.rank_