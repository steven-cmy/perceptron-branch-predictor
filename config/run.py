from __future__ import print_function

import argparse
import m5
from m5.objects import TimingSimpleCPU, DerivO3CPU
from m5.objects import PerceptronBranchPredictor, LocalBP, BiModeBP, TournamentBP
from m5.objects import Root
from m5.objects import *
import time
from system import BaseTestSystem

valid_cpus = [DerivO3CPU, TimingSimpleCPU]
valid_cpus = {cls.__name__[:-3]: cls for cls in valid_cpus}
valid_bp = [PerceptronBranchPredictor, LocalBP, BiModeBP, TournamentBP]
valid_bp = {cls.__name__: cls for cls in valid_bp}


parser = argparse.ArgumentParser()
parser.add_argument('cpu', choices=valid_cpus.keys())
parser.add_argument('bp', choices=valid_bp.keys())
parser.add_argument('pdepth', type=int, default=64,
                    help="Depth of perceptron when using perceptron branch predictor")
parser.add_argument('pprime', type=int, default=61,
                    help="Prime number to determine index  when using perceptron branch predictor(ideally the largest prime smaller than depth)")
parser.add_argument('binary', type=str, help="Path to binary to run")
# parser.add_argument("--clock", action="store",
#                       default='1GHz',
#                       help = """Top-level clock for blocks running at system
#                       speed""")
args = parser.parse_args()


class PBPTestSystem(BaseTestSystem):
    _CPUModel = valid_cpus[args.cpu]
    _BPredictor = valid_bp[args.bp]
    _PerceptronDepth = args.pdepth
    _PerceptronPrime = args.pprime


system = PBPTestSystem()
system.setTestBinary(args.binary)
root = Root(full_system=False, system=system)
m5.instantiate()

start_tick = m5.curTick()
start_insts = system.totalInsts()
globalStart = time.time()
exit_event = m5.simulate()


print("Exit Event" + exit_event.getCause())
if exit_event.getCause() == "workbegin":
    # Reached the start of ROI
    # start of ROI is marked by an
    # m5_work_begin() call
    m5.stats.reset()
    start_tick = m5.curTick()
    start_insts = system.totalInsts()
    print("Resetting stats at the start of ROI!")
    exit_event = m5.simulate()

# Reached the end of ROI
# Finish executing the benchmark with kvm cpu
if exit_event.getCause() == "workend":
    # Reached the end of ROI
    # end of ROI is marked by an
    # m5_work_end() call
    print("Dump stats at the end of the ROI!")
    m5.stats.dump()
    end_tick = m5.curTick()
    end_insts = system.totalInsts()
    m5.stats.reset()
else:
    print("Terminated simulation before reaching ROI!")
    m5.stats.dump()
    end_tick = m5.curTick()
    end_insts = system.totalInsts()
    print("Performance statistics:")
    print("Simulated time: %.2fs" % ((end_tick-start_tick)/1e12))
    print("Instructions executed: %d" % ((end_insts-start_insts)))
    print("Ran a total of", m5.curTick()/1e12, "simulated seconds")
    print("Total wallclock time: %.2fs, %.2f min" %
          (time.time()-globalStart, (time.time()-globalStart)/60))
    exit()
