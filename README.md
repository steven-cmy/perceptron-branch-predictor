# perceptron-branch-predictor
Implemtation of a Perceptron Branch Predictor on gem5 simulator.
## Getting Started

### Get gem5
``` bash
git clone git@github.com:CMPT-7ARCH-SFU/gem5-baseline.git gem5
# Alternativly you can use official gem5
# git clone https://github.com/gem5/gem5 gem5
export M5_PATH=gem5
```

### Integrating the predictor
``` bash
python3 install.py gem5/src src
# This will hard link our code to gem5's src
```

### Build gem5
``` bash
cd gem5 
## Stop git tracking large file changes. Add --global if you want to turn off for all.
git config oh-my-zsh.hide-info 1
# First build might take a long time
# on 10 cores it may take 15 minutes
# Open a tmux session. 
scons build/X86/gem5.opt -j 8

# every time src change you need rebuild
```

### Using SPEC 2017

#### Automaic with script

``` bash
# adjust benchmarks in the script if you want
# this will take ~10mins
./build_benchmarks.sh
# workload instructions will be output to $REPO/bin
```

#### Manual way

To install SPEC 2017
``` bash
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
``` bash
go <BENCHMARK_NAME>
rm -r build
runcpu --fake --config gcc-linux-x86 <BENCHMARK_NAME>
cd build/build_base_<CONFIG_LABEL>-m64.0000
specmake [TARGET=BENCHMARK_NAME] -j 8
cd ../../run/run_base_refspeed_<CONFIG_LABEL>-m64.0000
specinvoke -n
# You should get instructions on how to run the benchmark
```

To run benchmark with gem5
``` bash
/where/gem5/is/build/X86/gem5.opt \
/where/gem5/is/configs/example/se.py \
-cmd=../../build/build_base_<CONFIG_LABEL>-m64.0000/<BENCHMARK_NAME> \
--options="<OPTION_YOU_GET_FROM_SPECINVOKE_GOES_HERE>" \
# gem5 config goes here
--mem-size=8GB \
--cpu-type=DerivO3CPU \
--caches --l2cache \
--l1d_size=32kB --l1i_size=32kB --l2_size=512kB
```

### Testing and Evaluating
``` bash
export M5_PATH=gem5
export SPEC_PATH=spec2017
export REPO=$(pwd)
# adjust config in the py file if needed
python3 run_benchamrks.py 8
# evaluation
python3 plot.py
```

Test result is stored in $REPO/results folder and plots are in $REPO.