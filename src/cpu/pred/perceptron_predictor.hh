#ifndef __CPU_PRED_PERCEPTRON_PREDICTOR_HH__
#define __CPU_PRED_PERCEPTRON_PREDICTOR_HH__

#include "cpu/pred/bpred_unit.hh"
#include "params/PerceptronBranchPredictor.hh"
#include <vector>

struct Perceptron
{
    std::vector<int> weight;
    int bias;

    Perceptron(int depth) : weight(depth, 0), bias(0) {}
};

struct BPHistory
{
    std::vector<bool> taken;

    BPHistory(int size) : taken(size, false) {}
};

bool isPrime(int number)
{
    if (number <= 1)
        return false;
    if (number <= 3)
        return true;

    if (number % 2 == 0 || number % 3 == 0)
        return false;

    for (int i = 5; i * i <= number; i += 6)
    {
        if (number % i == 0 || number % (i + 2) == 0)
            return false;
    }
    return true;
}

int largestPrimeLessThan(int X)
{
    for (int i = X; i > 1; --i)
    {
        if (isPrime(i))
        {
            return i;
        }
    }
    exit(-1); // Return -1 if no prime number is found
}

class PerceptronBranchPredictor : public BPredUnit
{
public:
    PerceptronBranchPredictor(const PerceptronBranchPredictorParams *params);

    unsigned hash(Addr branchAddr) { return branchAddr % this->PRIME; }

    bool lookup(ThreadID tid, Addr branchAddr, void *&bpHistory) override;
    void update(ThreadID tid, Addr branchAddr, bool taken,
                void *bpHistory, bool squashed,
                const StaticInstPtr &inst,
                Addr corrTarget) override;
    void squash(ThreadID tid, void *bpHistory) override;
    void uncondBranch(ThreadID tid, Addr pc, void *&bp_history) override;
    void btbUpdate(ThreadID tid, Addr instPC, void *&bp_history) override;

protected:
    void updatePerceptron(Addr branchAddr, bool taken, void *bpHistory);

    std::vector<Perceptron> perceptrons;
    unsigned N;
    unsigned PRIME;
};

#endif // __CPU_PRED_PERCEPTRON_PREDICTOR_HH__
