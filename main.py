from sweep import Sweep
from sweepPlayer import SweepPlayer
from randomPlayer import RandomPlayer

sweep = Sweep()
sweep.play([RandomPlayer, SweepPlayer])
