# perceptron-branch-predictor
Implemtation of a Perceptron Branch Predictor on gem5 simulator.
## Getting Started
### Build gem5
```
git clone git@github.com:CMPT-7ARCH-SFU/gem5-baseline.git gem5
cd gem5 
## Stop git tracking large file changes. Add --global if you want to turn off for all.
git config oh-my-zsh.hide-info 1
# First build might take a long time
# on 10 cores it may take 15 minutes
# Open a tmux session. 
scons -j 8 build/RISCV/gem5.opt CPU_MODELS='AtomicSimpleCPU,O3CPU,TimingSimpleCPU,MinorCPU' --gold-linker
```

### Using SPEC 2017
To install SPEC 2017
```
cp -r /data/shared/spec2017/spec2017 spec2017
cd spec2017
cp config/Example-gcc-linux-x86.cfg config/gcc-linux-x86.cfg

# Edit all EDIT marks
code !$
which gcc
gcc --version

./install.sh
source ./shrc
bin/packagetools gcc-linux-x86
```
To build a benchmark
```
go <benchamrk_name>
rm -r build
runcpu --fake --config gcc-linux-x86 <benchamrk_name>
cd build/build_base_<config_label>-m64.0000
specmake [TARGET=benchamrk_name] -j 8
cd ../../run/run_base_refspeed_<config_label>-m64.0000
specinvoke -n
# You should get instruction on how to run the benchmark
```

To run benchmark with gem5
```
/where/gem5/is/build/X86/gem5.opt \
/where/gem5/is/configs/example/se.py \
-cmd=../../build/build_base_<config_label>-m64.0000/<benchmark_name> \
--options="<option you get from specinvoke goes here>" \
# gem5 config goes here
--mem-size=8GB \
--cpu-type=DerivO3CPU \
--caches --l2cache \
--l1d_size=32kB --l1i_size=32kB --l2_size=512kB
```

### Running gem5
```
cd $REPO
gem5-baseline/build/RISCV/gem5.opt gem5-baseline/configs/learning_gem5/part1/simple.py
```
### Integrating the predictor
```
TODO
```
### Testing and Evaluating
```
TODO
```