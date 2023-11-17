#include "cpu/pred/perceptron_predictor.hh"

PerceptronBranchPredictor::PerceptronBranchPredictor(const PerceptronBranchPredictorParams *params)
    : BPredUnit(params)
{
    N = params->perceptron_depth;
    PRIME = largestPrimeLessThan(N);

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
    // Implement the update logic here
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

void uncondBranch(ThreadID tid, Addr pc, void *&bp_history)
{
    // Implement the function
}

void btbUpdate(ThreadID tid, Addr instPC, void *&bp_history)
{
    // Implement the function
}
void squash(ThreadID tid, void *bpHistory)
{
}

PerceptronBranchPredictor *
PerceptronBranchPredictorParams::create()
{
    return new PerceptronBranchPredictor(this);
}
