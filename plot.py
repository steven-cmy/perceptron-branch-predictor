import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import os

if not os.getenv("REPO"):
    print("Set repo path\n")
    exit(1)

workload_dir = os.getenv("REPO") + '/bin'
datadir = os.getenv("REPO") + '/results/X86/run'
outputdir = os.getenv("REPO") + '/plots'


def gem5GetStat(filename, stat):
    filename = os.path.join(datadir, '', filename,
                            'stats.txt').replace('\\', '/')
    with open(filename) as f:
        r = f.read()
        if len(r) < 10:
            return 0.0
        if (r.find(stat) != -1):
            start = r.find(stat) + len(stat) + 1
            end = r.find('#', start)
            # print(r[start:end])
            return float(r[start:end])
        else:
            return float(0.0)


cpu_types = ['DerivO3']
branch_predictors = ['LocalBP', 'BiModeBP',
                     'TournamentBP', 'PerceptronBranchPredictor']
benchmarks = []

if not os.path.exists(datadir):
    exit("You need to run benchamrks first!")

for bm in os.listdir(workload_dir):
    if not os.path.isdir(f'{workload_dir}/{bm}'):
        benchmarks.append(bm)

rows = []

for bm in benchmarks:
    for cpu in cpu_types:
        for bp in branch_predictors:
            rows.append([bm, cpu, bp,
                         gem5GetStat(datadir+"/"+bm+"/"+"/"+cpu +
                                     "/"+bp+"/b", 'system.cpu.numCycles'),
                         gem5GetStat(datadir+"/"+bm+"/"+"/"+cpu +
                                     "/"+bp+"/b", 'sim_insts'),
                         gem5GetStat(datadir+"/"+bm+"/"+"/"+cpu+"/"+bp +
                                     "/b", 'system.cpu.branchPred.condPredicted'),
                         gem5GetStat(datadir+"/"+bm+"/"+"/"+cpu+"/"+bp +
                                     "/b", 'system.cpu.branchPred.condIncorrect'),
                         gem5GetStat(datadir+"/"+bm+"/"+"/"+cpu+"/"+bp +
                                     "/b", 'system.cpu.commit.commitSquashedInsts'),
                         ])

df = pd.DataFrame(rows, columns=['benchmark', 'cpu', 'bp', 'cycles',
                  'instructions', 'totalPrediction', 'incorrectPrediction','squashedInsts'])
df['ipc'] = df['instructions']/df['cycles']
df['cpi'] = 1/df['ipc']
df['accuracy'] = (df['totalPrediction'] -
                  df['incorrectPrediction'])/df['totalPrediction']
# print(df)


def draw_vertical_line(ax, xpos, ypos):
    line = plt.Line2D([xpos, xpos], [ypos + .1, ypos],
                      transform=ax.transAxes, color='black', lw=1)
    line.set_clip_on(False)
    ax.add_line(line)


def doplot_benchmarks(benchmarks, stat, norm=True):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    i = 0
    for bm in benchmarks:
        base = df[(df['benchmark'] == bm)][stat].iloc[0] if norm else 1
        for c, sys in enumerate(cpu_types):
            for b, bp in enumerate(branch_predictors):
                d = df[(df['benchmark'] == bm) & (
                    df['cpu'] == sys) & (df['bp'] == bp)]
                # print(d)
                ax.bar(i, d[stat].iloc[0]/base, color='C'+str(c*4+b))
                i += 1
        i += 1
    for c, cpu in enumerate(cpu_types):
        for b, bp in enumerate(branch_predictors):
            plt.bar(0, 0, color='C'+str(c*4+b), label=cpu+'/'+bp)
    new_names = benchmarks
    # Arranging ticks on the X axis
    plt.xticks(np.arange(len(new_names))*(len(cpu_types)*len(branch_predictors)+1) +
               (len(cpu_types)*len(branch_predictors)-1)/2, new_names, rotation=40, ha='right')


stats = [
    'accuracy',
    'ipc',
    # 'cpi',
    'squashedInsts'
    ]
for stat in stats:
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 10
    fig_size[1] = 5
    plt.rcParams["figure.figsize"] = fig_size
    fig1 = doplot_benchmarks(benchmarks, stat, norm=False)
    # plt.ylabel(stat)
    plt.legend(loc=2, prop={'size': 8})
    plt.title(stat.capitalize())
    plt.tight_layout()
    plt.savefig(stat+'.png', format='png', dpi=600)
