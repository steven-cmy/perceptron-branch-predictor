from run import gem5Run
import os
import sys
from uuid import UUID
from itertools import starmap
from itertools import product
import multiprocessing as mp
import argparse


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
    branch_predictors = ['LocalBP','BiModeBP','TournamentBP','PerceptronBranchPredictor']
    benchmarks = []

    if not os.path.exists('bin'):
        exit("You need to build benchamrk binaries first!")

    for filename in os.listdir('bin'):
        if not os.path.isdir(f'bin/{filename}'):
            benchmarks.append(filename)

    jobs = []
    for bm in benchmarks:
        for cpu in cpu_types:
            for bp in branch_predictors:
                run = gem5Run.createSERun(
                    'branch_predictor_tests',
                    os.getenv('M5_PATH')+'/build/X86/gem5.opt',
                    'config/run.py',
                    'results/X86/run/{}/{}/{}/b'.format(
                        bm, cpu, bp),
                    cpu, bp, '64', '61',
                    os.path.join('bin', bm))
                jobs.append(run)

    with mp.Pool(args.N) as pool:
        pool.map(worker, jobs)
