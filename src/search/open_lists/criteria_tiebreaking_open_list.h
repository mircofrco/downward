#ifndef OPEN_LISTS_CRITERIA_TIEBREAKING_OPEN_LIST_H
#define OPEN_LISTS_CRITERIA_TIEBREAKING_OPEN_LIST_H

#include "../open_list_factory.h"

namespace criteria_tiebreaking_open_list {

enum class TieBreakingCriteria {
    FIFO,
    LIFO,
    RANDOM
};

class CriteriaTieBreakingOpenListFactory : public OpenListFactory {
    std::vector<std::shared_ptr<Evaluator>> evals;
    bool unsafe_pruning;
    bool pref_only;
    TieBreakingCriteria tiebreaking_criteria;
public:
    CriteriaTieBreakingOpenListFactory(
        const std::vector<std::shared_ptr<Evaluator>> &evals,
        bool unsafe_pruning, bool pref_only, const TieBreakingCriteria tiebreaking_criteria);

    virtual std::unique_ptr<StateOpenList> create_state_open_list() override;
    virtual std::unique_ptr<EdgeOpenList> create_edge_open_list() override;
};

}




#endif
