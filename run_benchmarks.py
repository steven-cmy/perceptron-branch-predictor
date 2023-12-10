from run import gem5Run
import os
import sys
from uuid import UUID
from itertools import starmap
from itertools import product
import multiprocessing as mp
import argparse


if not os.getenv("REPO"):
    print("Set REPO Path!\n")
    exit(1)
if not os.getenv("M5_PATH"):
    print("Set gem5 Path!\n")
    exit(1)
if not os.getenv("SPEC_PATH"):
    print("Set SPEC Path!\n")
    exit(1)


def worker(run):
    run.run()
    json = run.dumpsJson()
    print(json)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('N', action="store",
                        default=1, type=int,
                        help="""Number of cores used for simulation""")
    args = parser.parse_args()

    cpu_types = ['DerivO3']
    branch_predictors = [
        'LocalBP',
        'BiModeBP',
        'TournamentBP',
        'PerceptronBranchPredictor'
        ]
    # benchmarks = ["505.mcf_r","520.omnetpp_r","525.x264_r","531.deepsjeng_r","600.perlbench_s","602.gcc_s","605.mcf_s","620.omnetpp_s","625.x264_s","631.deepsjeng_s"]
    benchmarks = []

    if not os.path.exists('bin'):
        exit("You need to build benchamrk binaries first!")

    for filename in os.listdir('bin'):
        if not os.path.isdir(f'bin/{filename}'):
            # if filename.endswith(".option"):
            # benchmarks.append(os.path.splitext(filename)[0])
            benchmarks.append(filename)

    perceptron_depth = 64
    saturation_limit = 16
    
    def is_prime(n):
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def largest_prime_smaller_than(x):
        for num in range(x - 1, 1, -1):
            if is_prime(num):
                return num
        return None
    
    jobs = []
    for bm in benchmarks:
        for cpu in cpu_types:
            for bp in branch_predictors:
                run = gem5Run.createSERun(
                    'branch_predictor_tests',
                    os.getenv('REPO')+'/'+os.getenv('M5_PATH')+'/build/X86/gem5.opt',
                    os.getenv('REPO')+'/'+'config/run.py',
                    os.getenv('REPO')+'/'+'results/X86/run/{}/{}/{}/b'.format(
                        bm, cpu, bp),
                    cpu, bp, str(perceptron_depth), str(largest_prime_smaller_than(perceptron_depth)), str(saturation_limit),
                    os.path.join(bm))
                jobs.append(run)

    with mp.Pool(args.N) as pool:
        pool.map(worker, jobs)
