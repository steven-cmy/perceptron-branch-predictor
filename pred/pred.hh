#ifndef __PERCEPTRON_PREDICTOR_HH__
#define __PERCEPTRON_PREDICTOR_HH__

#include "cpu/pred/bpred_unit.hh"

class PerceptronBranchPredictor : public BPredUnit
{
public:
    PerceptronBranchPredictor(const PerceptronBranchPredictorParams *params);

    bool lookup(ThreadID tid, Addr branchAddr, void *&bpHistory) override;
    void update(ThreadID tid, Addr branchAddr, bool taken,
                void *bpHistory, bool squashed,
                const StaticInstPtr &inst,
                Addr corrTarget) override;
    void squash(ThreadID tid, void *bpHistory) override;

protected:
    // Add your predictor's specific data structures here
};

#endif // __PERCEPTRON_PREDICTOR_HH__
