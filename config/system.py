from __future__ import print_function
from __future__ import absolute_import


# import the m5 (gem5) library created when gem5 is built
import m5
# import all of the SimObjects
from m5.objects import *


class BaseTestSystem(System):
    _CPUModel = DerivO3CPU
    _Clk = "1GHz"
    _BPredictor = PerceptronBranchPredictor
    _PerceptronDepth = 64
    _PerceptronPrime = 61
    # _L1DCacheSize = "32kB"
    # _L1DCacheAssoc = 1
    # _L2CacheSize = "1MB"
    # _L2CacheAssoc = 1
    # #_L1ICacheSize = "32kB"
    # _DRAMModel = "DDR4_2400_16x4"

    def __init__(self):
        self.exit_on_work_items = True
        super(BaseTestSystem, self).__init__()
        self.clk_domain = SrcClockDomain(
            clock=self._Clk, voltage_domain=VoltageDomain())
        self.exit_on_work_items = True
        self.mem_mode = 'timing'
        self.mem_ranges = [AddrRange('2GB')]

        self.cpu = self._CPUModel()
        self.cpu.branchPred = self._BPredictor()
        if self._BPredictor is PerceptronBranchPredictor:
            self.cpu.branchPred.perceptron_depth = self._PerceptronDepth
            self.cpu.branchPred.prime = self._PerceptronPrime

        self.membus = SystemXBar()

        self.cpu.icache_port = self.membus.slave
        self.cpu.dcache_port = self.membus.slave

        self.cpu.createInterruptController()

        if m5.defines.buildEnv['TARGET_ISA'] == "x86":
            self.cpu.interrupts[0].pio = self.membus.master
            self.cpu.interrupts[0].int_master = self.membus.slave
            self.cpu.interrupts[0].int_slave = self.membus.master

        self.mem_ctrl = MemCtrl()
        self.mem_ctrl.dram = DDR4_2400_16x4()
        self.mem_ctrl.dram.range = self.mem_ranges[0]
        self.mem_ctrl.port = self.membus.master

        self.system_port = self.membus.slave

    def totalInsts(self):
        return sum([cpu.totalInsts() for cpu in self.cpu])

    def addTestWorkload(self, pid, cmd, cwd):
        self.cpu.workload.append(Process(pid=pid, cmd=cmd, cwd=cwd))
