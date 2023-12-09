from __future__ import print_function

import argparse
import os
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
parser.add_argument('workloads', type=str, help="Path to the workload to run")
args = parser.parse_args()


class PBPTestSystem(BaseTestSystem):
    _CPUModel = valid_cpus[args.cpu]
    _BPredictor = valid_bp[args.bp]
    _PerceptronDepth = args.pdepth
    _PerceptronPrime = args.pprime


system = PBPTestSystem()

i = len(valid_bp.keys())
for k in valid_bp.keys():
    if k == args.bp:
        break
    i -= 1

bm_name = args.workloads
wl_file = os.path.join(os.getenv('REPO'), 'bin', bm_name)
cwd = os.path.join(os.getenv('REPO'), os.getenv('SPEC_PATH'),
                   'benchspec', 'CPU', bm_name, 'run', 'run_base_refspeed_pbptest-m64.0000'if bm_name.endswith('s') else 'run_base_refrate_pbptest-m64.0000')
os.chdir(cwd)
workloads = []
with open(wl_file, 'r') as workloadFile:
    lines = workloadFile.readlines()
    for line in lines:
        if not line.startswith('#') and not line.startswith('specinvoke'):
            cmd = line.split(' ')
            pid = int(bm_name.split('.', 1)[0]+str(i))
            system.addTestWorkload(pid, cmd, cwd)
            break
system.cpu.createThreads()
root = Root(full_system=False, system=system)
system.cpu.max_insts_any_thread = 2000000
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
