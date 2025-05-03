#include "criteria_tiebreaking_open_list.h"

#include "../evaluator.h"
#include "../open_list.h"

#include "../plugins/plugin.h"
#include "../utils/memory.h"

#include <cassert>
#include <deque>
#include <map>
#include <utility>
#include <vector>
#include <optional>
#include <cstdlib>
#include <ctime>
#include <iterator>

using namespace std;

namespace criteria_tiebreaking_open_list {
template<class Entry>
class CriteriaTieBreakingOpenList : public OpenList<Entry> {
    using Bucket = deque<Entry>;

    map<const vector<int>, Bucket> buckets;
    int size;

    vector<shared_ptr<Evaluator>> evaluators;
    /*
      If allow_unsafe_pruning is true, we ignore (don't insert) states
      which the first evaluator considers a dead end, even if it is
      not a safe heuristic.
    */
    bool allow_unsafe_pruning;

    TieBreakingCriteria tiebreaking_criteria;

    int dimension() const;

protected:
    void do_insertion(EvaluationContext &eval_context,
                          const Entry &entry) override;

public:
    CriteriaTieBreakingOpenList(
        const vector<shared_ptr<Evaluator>> &evals,
        bool unsafe_pruning, bool pref_only, const TieBreakingCriteria tiebreaking_criteria); // TODO: default enum

    virtual Entry remove_min() override;
    virtual bool empty() const override;
    virtual void clear() override;
    virtual void get_path_dependent_evaluators(set<Evaluator *> &evals) override;
    virtual bool is_dead_end(
        EvaluationContext &eval_context) const override;
    virtual bool is_reliable_dead_end(
        EvaluationContext &eval_context) const override;
};


template<class Entry>
CriteriaTieBreakingOpenList<Entry>::CriteriaTieBreakingOpenList( // Constructor when criteria is used
    const vector<shared_ptr<Evaluator>> &evals,
    bool unsafe_pruning, bool pref_only, const TieBreakingCriteria tiebreaking_criteria)
    : OpenList<Entry>(pref_only),
      size(0), evaluators(evals),
      allow_unsafe_pruning(unsafe_pruning),
      tiebreaking_criteria(tiebreaking_criteria) {
}

template<class Entry>
void CriteriaTieBreakingOpenList<Entry>::do_insertion(
        EvaluationContext &eval_context, const Entry &entry) {
    vector<int> key;
    key.reserve(evaluators.size());
    for (const shared_ptr<Evaluator> &evaluator : evaluators)
        key.push_back(eval_context.get_evaluator_value_or_infinity(evaluator.get()));

    buckets[key].push_back(entry);
    ++size;
}

template<class Entry>
Entry CriteriaTieBreakingOpenList<Entry>::remove_min() {
    assert(size > 0);
    typename map<const vector<int>, Bucket>::iterator it;
    it = buckets.begin();
    assert(it != buckets.end());
    assert(!it->second.empty());
    --size;

    std::optional<Entry> result;
    auto it_elem = it->second.end();

    switch(tiebreaking_criteria) {
    case TieBreakingCriteria::FIFO:
        result = it->second.front();
        it->second.pop_front();
        break;
    case TieBreakingCriteria::LIFO:
        result = it->second.back();
        it->second.pop_back();
        break;
    case TieBreakingCriteria::RANDOM:
        srand(time(nullptr));
        int pos;
        int i;
        i = it->second.size();
        pos = (rand() % i);
        it_elem = it->second.begin() + pos;
        result = *it_elem;
        it->second.erase(it_elem);
        break;
    default:
        cout << "Tie-breaking criteria was not found. Using default FIFO." << std::endl;
        Entry result = it->second.front();
        it->second.pop_front();
    }


    if (it->second.empty())
        buckets.erase(it);

    return *result;
}

template<class Entry>
bool CriteriaTieBreakingOpenList<Entry>::empty() const {
    return size == 0;
}

template<class Entry>
void CriteriaTieBreakingOpenList<Entry>::clear() {
    buckets.clear();
    size = 0;
}

template<class Entry>
int CriteriaTieBreakingOpenList<Entry>::dimension() const {
    return evaluators.size();
}

template<class Entry>
void CriteriaTieBreakingOpenList<Entry>::get_path_dependent_evaluators(
    set<Evaluator *> &evals) {
    for (const shared_ptr<Evaluator> &evaluator : evaluators)
        evaluator->get_path_dependent_evaluators(evals);
}

template<class Entry>
bool CriteriaTieBreakingOpenList<Entry>::is_dead_end(
    EvaluationContext &eval_context) const {
    // TODO: Properly document this behaviour.
    // If one safe heuristic detects a dead end, return true.
    if (is_reliable_dead_end(eval_context))
        return true;
    // If the first heuristic detects a dead-end and we allow "unsafe
    // pruning", return true.
    if (allow_unsafe_pruning &&
        eval_context.is_evaluator_value_infinite(evaluators[0].get()))
        return true;
    // Otherwise, return true if all heuristics agree this is a dead-end.
    for (const shared_ptr<Evaluator> &evaluator : evaluators)
        if (!eval_context.is_evaluator_value_infinite(evaluator.get()))
            return false;
    return true;
}

template<class Entry>
bool CriteriaTieBreakingOpenList<Entry>::is_reliable_dead_end(
    EvaluationContext &eval_context) const {
    for (const shared_ptr<Evaluator> &evaluator : evaluators)
        if (eval_context.is_evaluator_value_infinite(evaluator.get()) &&
            evaluator->dead_ends_are_reliable())
            return true;
    return false;
}

CriteriaTieBreakingOpenListFactory::CriteriaTieBreakingOpenListFactory(
    const vector<shared_ptr<Evaluator>> &evals,
    bool unsafe_pruning, bool pref_only, const TieBreakingCriteria tiebreaking_criteria)
    : evals(evals),
      unsafe_pruning(unsafe_pruning),
      pref_only(pref_only),
      tiebreaking_criteria(tiebreaking_criteria) {
}

unique_ptr<StateOpenList>
CriteriaTieBreakingOpenListFactory::create_state_open_list() {
    return utils::make_unique_ptr<CriteriaTieBreakingOpenList<StateOpenListEntry>>(
        evals, unsafe_pruning, pref_only, tiebreaking_criteria);
}

unique_ptr<EdgeOpenList>
CriteriaTieBreakingOpenListFactory::create_edge_open_list() {
    return utils::make_unique_ptr<CriteriaTieBreakingOpenList<EdgeOpenListEntry>>(
        evals, unsafe_pruning, pref_only, tiebreaking_criteria);
}

class CriteriaTieBreakingOpenListFeature
    : public plugins::TypedFeature<OpenListFactory, CriteriaTieBreakingOpenListFactory> {
public:
    CriteriaTieBreakingOpenListFeature() : TypedFeature("criteria_tiebreaking") {
        document_title("Tie-breaking open list");
        document_synopsis("");

        add_list_option<shared_ptr<Evaluator>>("evals", "evaluators");
        add_option<bool>(
            "unsafe_pruning",
            "allow unsafe pruning when the main evaluator regards a state a dead end",
            "true");
        add_option<TieBreakingCriteria>(
            "tiebreaking_criteria",
            "Choose between 'fifo' (First-In-First-Out), 'lifo' (Last-In-First-Out) or at random",
            "fifo");
        add_open_list_options_to_feature(*this);
    }

    virtual shared_ptr<CriteriaTieBreakingOpenListFactory> create_component(
        const plugins::Options &opts,
        const utils::Context &context) const override {
        plugins::verify_list_non_empty<shared_ptr<Evaluator>>(
            context, opts, "evals");
        return plugins::make_shared_from_arg_tuples<CriteriaTieBreakingOpenListFactory>(
            opts.get_list<shared_ptr<Evaluator>>("evals"),
            opts.get<bool>("unsafe_pruning"),
            get_open_list_arguments_from_options(opts),
            opts.get<TieBreakingCriteria>("tiebreaking_criteria")
            );
    }
};

static plugins::FeaturePlugin<CriteriaTieBreakingOpenListFeature> _plugin;

static plugins::TypedEnumPlugin<TieBreakingCriteria> _enum_plugin({
        {"fifo", "tiebreaking with First-In-First-Out"},
        {"lifo", "tiebreaking with Last-In-First-Out"},
        {"random", "tiebreaking at random"}
});
}
