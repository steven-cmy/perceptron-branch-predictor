#ifndef __CPU_PRED_PERCEPTRON_PREDICTOR_HH__
#define __CPU_PRED_PERCEPTRON_PREDICTOR_HH__

#include "cpu/pred/bpred_unit.hh"
#include "params/PerceptronBranchPredictor.hh"

class PerceptronBranchPredictor : public BPredUnit
{
public:
    PerceptronBranchPredictor(const PerceptronBranchPredictorParams *params);
    void uncondBranch(ThreadID tid, Addr pc, void *&bp_history);
    void squash(ThreadID tid, void *bp_history);
    bool lookup(ThreadID tid, Addr branch_addr, void *&bp_history);
    void btbUpdate(ThreadID tid, Addr branch_addr, void *&bp_history);
    void update(ThreadID tid, Addr branch_addr, bool taken, void *bp_history,
                bool squashed, const StaticInstPtr &inst, Addr corrTarget);

private:
    void updatePerceptron(Addr branchAddr, bool taken, void *bpHistory);

    struct BPHistory
    {
        std::vector<bool> taken;

        BPHistory(int size) : taken(size, false) {}
    };

    struct Perceptron
    {
        std::vector<int> weight;
        int bias;

        Perceptron(int depth) : weight(depth, 0), bias(0) {}
    };

    std::vector<Perceptron> perceptrons;
    unsigned N;
    unsigned PRIME;
    unsigned hash(Addr branchAddr) { return branchAddr % this->PRIME; }
    
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

    void insert(BPHistory history, bool taken)
    {
        if (history.taken.size()==N)
            history.taken.erase(history.taken.begin());
        history.taken.push_back(taken);
    }
};

#endif // __CPU_PRED_PERCEPTRON_PREDICTOR_HH__
