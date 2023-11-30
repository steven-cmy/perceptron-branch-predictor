#include "cpu/pred/perceptron_predictor.hh"

PerceptronBranchPredictor::PerceptronBranchPredictor(const PerceptronBranchPredictorParams *params)
    : BPredUnit(params)
{
    N = params->perceptron_depth;
    PRIME = (isPrime(params->prime) ? params->prime : largestPrimeLessThan(N));

    // Initialize your predictor's data structures here
    perceptrons = std::vector<Perceptron>(N, Perceptron(N));
    // for (auto &perceptron : perceptrons)
    // {
    //     perceptron = Perceptron(N);
    // }
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
    BPHistory *h = static_cast<BPHistory *>(bpHistory);

    int y = p.bias;
    for (unsigned n = 0; n < N; n++)
    {
        y += (h->taken[n] ? p.weight[n] : -p.weight[n]);
    }
    return ((y < 0) ? false : true);
}

void PerceptronBranchPredictor::update(ThreadID tid, Addr branchAddr, bool taken,
                                       void *bpHistory, bool squashed,
                                       const StaticInstPtr &inst, Addr corrTarget)
{
    updatePerceptron(branchAddr, taken, bpHistory);
}

void PerceptronBranchPredictor::uncondBranch(ThreadID tid, Addr pc, void *&bp_history)
{
    BPHistory *history = static_cast<BPHistory *>(bp_history);
    for (int i = N - 1; i > 0; i--)
    {
        history->taken[i] = history->taken[i - 1];
    }
    history->taken[0] = true;
}

void PerceptronBranchPredictor::btbUpdate(ThreadID tid, Addr instPC, void *&bp_history)
{
    updatePerceptron(instPC, false, bp_history);
}

void PerceptronBranchPredictor::squash(ThreadID tid, void *bpHistory)
{
    bpHistory = static_cast<BPHistory *>(bpHistory);
    delete[] bpHistory;
    bpHistory = new BPHistory(N);
}

void PerceptronBranchPredictor::updatePerceptron(Addr branchAddr, bool taken, void *bpHistory)
{
    assert(bpHistory);

    BPHistory *history = static_cast<BPHistory *>(bpHistory);
    Perceptron &p = perceptrons[hash(branchAddr)];

    p.bias += (taken ? 1 : -1);
    for (unsigned n = 0; n < N; n++)
    {
        p.weight[n] += ((history->taken[n] == taken) ? 1 : -1);
    }

    for (int i = N - 1; i > 0; i--)
    {
        history->taken[i] = history->taken[i - 1];
    }
    history->taken[0] = taken;
}

PerceptronBranchPredictor *
PerceptronBranchPredictorParams::create()
{
    return new PerceptronBranchPredictor(this);
}
