#!/bin/bash

REPO=$(cd $(dirname $0) && pwd)

if ! [ -d "bin" ]; then
    mkdir -p bin
fi

if ! [ -d "spec2017" ]; then
    cp -r /data/shared/spec2017/spec2017 spec2017
    cd spec2017
    ./install.sh
    cd ..
fi

cd spec2017
cp $REPO/gcc-linux-x86.cfg config/gcc-linux-x86.cfg
source ./shrc
bin/packagetools gcc-linux-x86

benchamrks=("505.mcf_r" "520.omnetpp_r" "525.x264_r" "531.deepsjeng_r" "600.perlbench_s" "602.gcc_s" "605.mcf_s" "620.omnetpp_s" "625.x264_s" "631.deepsjeng_s")
for benchmark in "${benchamrks[@]}"; do
    go $benchmark
    rm -r build
    runcpu --fake --config gcc-linux-x86 $benchmark
    cd build/build_base_pbptest-m64.0000
    specmake -j 8 || specmake TARGET=${benchmark#*.} -j 8
    cp ${benchmark#*.} $REPO/bin/${benchmark#*.}
done
