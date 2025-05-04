#include "div_tiebreaking_open_list.h"

#include "../evaluator.h"
#include "../open_list.h"
#include "selector.h"

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

namespace div_tiebreaking_open_list {
template<class Entry>
class DivTieBreakingOpenList : public OpenList<Entry> {
    using DepthBucket = deque<Entry>;
    //using Bucket = map<int, DepthBucket>;

    map<const vector<int>, Selector<Entry>> buckets;
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

    void div_do_insertion(EvaluationContext &eval_context,
                          const Entry &entry, EvaluationContext &parent_eval_context, int d_val);

protected:
    void do_insertion(EvaluationContext &eval_context,
                          const Entry &entry) override;

public:
    DivTieBreakingOpenList(
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
    void insert(EvaluationContext &eval_context, const Entry &entry, EvaluationContext &parent_eval_context, int d_val) override;
};


template<class Entry>
DivTieBreakingOpenList<Entry>::DivTieBreakingOpenList( // Constructor when criteria is used
    const vector<shared_ptr<Evaluator>> &evals,
    bool unsafe_pruning, bool pref_only, const TieBreakingCriteria tiebreaking_criteria)
    : OpenList<Entry>(pref_only),
      size(0), evaluators(evals),
      allow_unsafe_pruning(unsafe_pruning),
      tiebreaking_criteria(tiebreaking_criteria) {
}

template<class Entry>
void DivTieBreakingOpenList<Entry>::div_do_insertion(
    EvaluationContext &eval_context, const Entry &entry, EvaluationContext &parent_eval_context, int d_val) {
    //TODO: actual stuff
    vector<int> key;
    int depth_index = d_val;
    if (d_val == -1) {
        key.reserve(evaluators.size());
        for (const shared_ptr<Evaluator> &evaluator : evaluators)
            key.push_back(eval_context.get_evaluator_value_or_infinity(evaluator.get()));
        eval_context.set_d_value(0);
        depth_index = 0;
    } else {
        int f_val = -1;
        int parent_f_val = -1;
        key.reserve(evaluators.size());
        std::string sum_check("sum");
        for (const shared_ptr<Evaluator> &evaluator : evaluators)
            if (sum_check.compare(evaluator->get_description()) == 0) { // check if the evaluator is the sum evaluator to get the f-value
                f_val = eval_context.get_evaluator_value_or_infinity(evaluator.get()); // for A* first takes sum[g + h] = f-value...
                key.push_back(f_val);
                parent_f_val = parent_eval_context.get_evaluator_value_or_infinity(evaluator.get());
            } else {
                key.push_back(eval_context.get_evaluator_value_or_infinity(evaluator.get())); // ...and then heuristic value h
            }

        if (f_val < 0 || parent_f_val < 0) {
            cerr << "The f_value or the parent_f_value could not be calculated in div_do_insertion()." <<endl;
            exit(-1);
        }

        if (eval_context.get_g_value() == parent_eval_context.get_g_value() && f_val == parent_f_val) { // if g and f are the same, then both are in same plateau
            eval_context.set_d_value(d_val+1); // set the d-val of the child node (or rather eval_context) to d + 1
            depth_index = d_val + 1;
        } else {
            eval_context.set_d_value(0); // else the child is not in the same plateau -> d_val = 0
            depth_index = 0;
        }
    }

    Selector<Entry> &selector = buckets[key];
    selector.add(entry, depth_index);
    ++size;
}

template<typename Entry>
void DivTieBreakingOpenList<Entry>::do_insertion(
        EvaluationContext &eval_context,
        const Entry &entry) {
    (void)eval_context;
    (void)entry;
    cerr << "This is just a dummy method for do_insertion in div_tiebreaking_open_list.cc, which should not be called!" <<endl;
    exit(-1);
}

template<class Entry>
void DivTieBreakingOpenList<Entry>::insert( // overrides already implemented method from open_list.h
        EvaluationContext &eval_context, const Entry &entry, EvaluationContext &parent_eval_context, int d_val) {
    if (false && !eval_context.is_preferred()) // Check for only_preferred is ignored as it is not relevant for the bachelor's thesis
        return;
    if (!is_dead_end(eval_context))
        div_do_insertion(eval_context, entry, parent_eval_context, d_val);
}

template<class Entry>
Entry DivTieBreakingOpenList<Entry>::remove_min() {
    assert(size > 0);

    auto it = buckets.begin();
    Selector<Entry> &selector = it->second;
    assert(!selector.empty());

    Entry result = it->second.remove_next(tiebreaking_criteria);
    --size;

    if (selector.empty()) {
        buckets.erase(it);
    }

    return result;
}

template<class Entry>
bool DivTieBreakingOpenList<Entry>::empty() const {
    return size == 0;
}

template<class Entry>
void DivTieBreakingOpenList<Entry>::clear() {
    buckets.clear();
    size = 0;
}

template<class Entry>
int DivTieBreakingOpenList<Entry>::dimension() const {
    return evaluators.size();
}

template<class Entry>
void DivTieBreakingOpenList<Entry>::get_path_dependent_evaluators(
    set<Evaluator *> &evals) {
    for (const shared_ptr<Evaluator> &evaluator : evaluators)
        evaluator->get_path_dependent_evaluators(evals);
}

template<class Entry>
bool DivTieBreakingOpenList<Entry>::is_dead_end(
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
bool DivTieBreakingOpenList<Entry>::is_reliable_dead_end(
    EvaluationContext &eval_context) const {
    for (const shared_ptr<Evaluator> &evaluator : evaluators)
        if (eval_context.is_evaluator_value_infinite(evaluator.get()) &&
            evaluator->dead_ends_are_reliable())
            return true;
    return false;
}

DivTieBreakingOpenListFactory::DivTieBreakingOpenListFactory(
    const vector<shared_ptr<Evaluator>> &evals,
    bool unsafe_pruning, bool pref_only, const TieBreakingCriteria tiebreaking_criteria)
    : evals(evals),
      unsafe_pruning(unsafe_pruning),
      pref_only(pref_only),
      tiebreaking_criteria(tiebreaking_criteria) {
}

unique_ptr<StateOpenList>
DivTieBreakingOpenListFactory::create_state_open_list() {
    return utils::make_unique_ptr<DivTieBreakingOpenList<StateOpenListEntry>>(
        evals, unsafe_pruning, pref_only, tiebreaking_criteria);
}

unique_ptr<EdgeOpenList>
DivTieBreakingOpenListFactory::create_edge_open_list() {
    return utils::make_unique_ptr<DivTieBreakingOpenList<EdgeOpenListEntry>>(
        evals, unsafe_pruning, pref_only, tiebreaking_criteria);
}

class DivTieBreakingOpenListFeature
    : public plugins::TypedFeature<OpenListFactory, DivTieBreakingOpenListFactory> {
public:
    DivTieBreakingOpenListFeature() : TypedFeature("div_tiebreaking") {
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

    virtual shared_ptr<DivTieBreakingOpenListFactory> create_component(
        const plugins::Options &opts,
        const utils::Context &context) const override {
        plugins::verify_list_non_empty<shared_ptr<Evaluator>>(
            context, opts, "evals");
        return plugins::make_shared_from_arg_tuples<DivTieBreakingOpenListFactory>(
            opts.get_list<shared_ptr<Evaluator>>("evals"),
            opts.get<bool>("unsafe_pruning"),
            get_open_list_arguments_from_options(opts),
            opts.get<TieBreakingCriteria>("tiebreaking_criteria")
            );
    }
};

static plugins::FeaturePlugin<DivTieBreakingOpenListFeature> _plugin;

static plugins::TypedEnumPlugin<TieBreakingCriteria> _enum_plugin({
        {"fifo", "tiebreaking with First-In-First-Out"},
        {"lifo", "tiebreaking with Last-In-First-Out"},
        {"random", "tiebreaking at random"}
});
}
