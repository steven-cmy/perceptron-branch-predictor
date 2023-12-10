#include "cpu/pred/perceptron_predictor.hh"

PerceptronBranchPredictor::PerceptronBranchPredictor(const PerceptronBranchPredictorParams *params)
    : BPredUnit(params),
      perceptrons(params->perceptron_depth, Perceptron(params->perceptron_depth)),
      N(params->perceptron_depth),
      PRIME(params->prime),
      LIMIT(params->saturation_limit)
{
    if (!(isPrime(PRIME)))
        fatal("Prime is not actually a prime number.\n");

    // PRIME = (isPrime(params->prime) ? params->prime : largestPrimeLessThan(N));

    // for (auto &perceptron : perceptrons)
    // {
    //     perceptron = Perceptron(N);
    // }
}

void PerceptronBranchPredictor::uncondBranch(ThreadID tid, Addr pc, void *&bpHistory)
{
    if (!bpHistory)
    {
        bpHistory = new BPHistory(N);
    }
    BPHistory *history = static_cast<BPHistory *>(bpHistory);
    insert(*history, true);
    // for (int i = N - 1; i > 0; i--)
    // {
    //     history->taken[i] = history->taken[i - 1];
    // }
    // history->taken[0] = true;
}

void PerceptronBranchPredictor::squash(ThreadID tid, void *bpHistory)
{
    assert(bpHistory);
    BPHistory *history = static_cast<BPHistory *>(bpHistory);
    delete history;
    bpHistory = new BPHistory(N);
}

bool PerceptronBranchPredictor::lookup(ThreadID tid, Addr branchAddr, void *&bpHistory)
{
    // Implement the prediction logic here
    // Return true for taken, false for not taken
    Perceptron &p = perceptrons[hash(branchAddr)];
    if (!bpHistory)
    {
        bpHistory = new BPHistory(N);
    }
    BPHistory *history = static_cast<BPHistory *>(bpHistory);

    int y = p.bias;
    for (unsigned n = 0; n < N; n++)
    {
        y += (history->taken[n] ? p.weight[n] : -p.weight[n]);
    }
    return ((y < 0) ? false : true);
}

void PerceptronBranchPredictor::btbUpdate(ThreadID tid, Addr instPC, void *&bp_history)
{
    updatePerceptron(instPC, false, bp_history);
}

void PerceptronBranchPredictor::update(ThreadID tid, Addr branchAddr, bool taken,
                                       void *bpHistory, bool squashed,
                                       const StaticInstPtr &inst, Addr corrTarget)
{
    updatePerceptron(branchAddr, taken, bpHistory);
}

void PerceptronBranchPredictor::updatePerceptron(Addr branchAddr, bool taken, void *bpHistory)
{
    assert(bpHistory);

    BPHistory *history = static_cast<BPHistory *>(bpHistory);
    Perceptron &p = perceptrons[hash(branchAddr)];

    p.bias += (taken ? 1 : -1);
    for (unsigned n = 0; n < N; n++)
    {
        if (std::abs(p.weight[n]))
            p.weight[n] += ((history->taken[n] == taken) ? 1 : -1);
    }

    insert(*history, taken);
}

PerceptronBranchPredictor *
PerceptronBranchPredictorParams::create()
{
    return new PerceptronBranchPredictor(this);
}
