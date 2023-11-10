# perceptron-branch-predictor
Implemtation of a Perceptron Branch Predictor on gem5 simulator.
## Getting Started
### Build gem5
```
git clone git@github.com:CMPT-7ARCH-SFU/gem5-baseline.git
cd gem5-baseline    
## Stop git tracking large file changes. Add --global if you want to turn off for all.
git config oh-my-zsh.hide-info 1
# First build might take a long time
# on 10 cores it may take 15 minutes
# Open a tmux session. 
scons -j 8 build/RISCV/gem5.opt CPU_MODELS='AtomicSimpleCPU,O3CPU,TimingSimpleCPU,MinorCPU' --gold-linker
```
### Running gem5
```
cd $REPO
gem5-baseline/build/RISCV/gem5.opt gem5-baseline/configs/learning_gem5/part1/simple.py
```