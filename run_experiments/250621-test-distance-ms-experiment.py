#! /usr/bin/env python
# -*- coding: utf-8 -*-

import common_setup
from common_setup import IssueConfig, IssueExperiment

import os

from lab.reports import Attribute
from lab.reports import arithmetic_mean

from downward.reports.absolute import AbsoluteReport

from lab.environments import LocalEnvironment, BaselSlurmEnvironment
from experimentparser import PlateauParser

# TODO: Enter git commit hash of code version you want to use.
REVISIONS = ["1250970671146f94691f5f3d2793462e0ea463d3"]
DRIVER_OPTIONS = ["--overall-time-limit", "5m"]
CONFIGS = [
    common_setup.IssueConfig(
        "f, h^, fifo",
        [
            "--search",
            "let(h, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(h_adapted, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h]), h_adapted], unsafe_pruning=false, tiebreaking_criteria=fifo), reopen_closed=true, f_eval=sum([g(), h]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^, lifo",
        [
            "--search",
            "let(h, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(h_adapted, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h]), h_adapted], unsafe_pruning=false, tiebreaking_criteria=lifo), reopen_closed=true, f_eval=sum([g(), h]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^, ro1",
        [
            "--search",
            "let(h, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(h_adapted, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h]), h_adapted], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^, ro2",
        [
            "--search",
            "let(h2, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(h_adapted2, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h2]), h_adapted2], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h2]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^, ro3",
        [
            "--search",
            "let(h3, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(h_adapted3, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h3]), h_adapted3], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h3]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^, ro4",
        [
            "--search",
            "let(h4, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(h_adapted4, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h4]), h_adapted4], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h4]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^, ro5",
        [
            "--search",
            "let(h5, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(h_adapted5, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h5]), h_adapted5], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h5]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^, ro6",
        [
            "--search",
            "let(h6, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(h_adapted6, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h6]), h_adapted6], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h6]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^, ro7",
        [
            "--search",
            "let(h7, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(h_adapted7, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h7]), h_adapted7], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h7]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^, ro8",
        [
            "--search",
            "let(h8, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(h_adapted8, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h8]), h_adapted8], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h8]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^, ro9",
        [
            "--search",
            "let(h9, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(h_adapted9, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h9]), h_adapted9], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h9]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^, ro0",
        [
            "--search",
            "let(h0, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(h_adapted0, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h0]), h_adapted0], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h0]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h, h^, fifo",
        [
            "--search",
            "let(h, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(h_adapted, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h]), h, h_adapted], unsafe_pruning=false, tiebreaking_criteria=fifo), reopen_closed=true, f_eval=sum([g(), h]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h, h^, lifo",
        [
            "--search",
            "let(h, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(h_adapted, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h]), h, h_adapted], unsafe_pruning=false, tiebreaking_criteria=lifo), reopen_closed=true, f_eval=sum([g(), h]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h, h^, ro1",
        [
            "--search",
            "let(h, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(h_adapted, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h]), h, h_adapted], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h, h^, ro2",
        [
            "--search",
            "let(h2, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(h_adapted2, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h2]), h2, h_adapted2], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h2]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h, h^, ro3",
        [
            "--search",
            "let(h3, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(h_adapted3, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h3]), h3, h_adapted3], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h3]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h, h^, ro4",
        [
            "--search",
            "let(h4, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(h_adapted4, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h4]), h4, h_adapted4], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h4]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h, h^, ro5",
        [
            "--search",
            "let(h5, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(h_adapted5, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h5]), h5, h_adapted5], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h5]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h, h^, ro6",
        [
            "--search",
            "let(h6, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(h_adapted6, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h6]), h6, h_adapted6], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h6]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h, h^, ro7",
        [
            "--search",
            "let(h7, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(h_adapted7, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h7]), h7, h_adapted7], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h7]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h, h^, ro8",
        [
            "--search",
            "let(h8, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(h_adapted8, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h8]), h8, h_adapted8], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h8]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h, h^, ro9",
        [
            "--search",
            "let(h9, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(h_adapted9, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h9]), h9, h_adapted9], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h9]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h, h^, ro0",
        [
            "--search",
            "let(h0, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(h_adapted0, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h0]), h0, h_adapted0], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h0]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^-ff, fifo",
        [
            "--search",
            "let(h, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(hff, ff(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h]), hff], unsafe_pruning=false, tiebreaking_criteria=fifo), reopen_closed=true, f_eval=sum([g(), h]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^-ff, lifo",
        [
            "--search",
            "let(h, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(hff, ff(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h]), hff], unsafe_pruning=false, tiebreaking_criteria=lifo), reopen_closed=true, f_eval=sum([g(), h]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^-ff, ro1",
        [
            "--search",
            "let(h, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(hff, ff(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h]), hff], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^-ff, ro2",
        [
            "--search",
            "let(h2, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(hff2, ff(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h2]), hff2], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h2]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^-ff, ro3",
        [
            "--search",
            "let(h3, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(hff3, ff(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h3]), hff3], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h3]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^-ff, ro4",
        [
            "--search",
            "let(h4, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(hff4, ff(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h4]), hff4], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h4]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^-ff, ro5",
        [
            "--search",
            "let(h5, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(hff5, ff(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h5]), hff5], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h5]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^-ff, ro6",
        [
            "--search",
            "let(h6, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(hff6, ff(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h6]), hff6], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h6]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^-ff, ro7",
        [
            "--search",
            "let(h7, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(hff7, ff(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h7]), hff7], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h7]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^-ff, ro8",
        [
            "--search",
            "let(h8, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(hff8, ff(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h8]), hff8], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h8]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^-ff, ro9",
        [
            "--search",
            "let(h9, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(hff9, ff(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h9]), hff9], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h9]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^-ff, ro0",
        [
            "--search",
            "let(h0, merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1,main_loop_max_time=150), let(hff0, ff(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h0]), hff0], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h0]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    # TODO: Add your configs.
]

BENCHMARKS_DIR = os.environ["DOWNWARD_BENCHMARKS"]
REPO_DIR = os.environ["DOWNWARD_REPO"]

#if common_setup.is_test_run():
#    SUITE = common_setup.IssueExperiment.DEFAULT_TEST_SUITE
#    ENVIRONMENT = LocalEnvironment(processes=2)
#else:
SUITE = common_setup.DEFAULT_TEST_SUITE
ENVIRONMENT = BaselSlurmEnvironment(
    # Choose between infai_1 or infai_2. Either works but stick to a
    # single partition when results have to be comparable.
    partition="infai_2",
    # TODO: Change this to your own email, you will get notified when your
    # jobs finish.
    email="m.franco@stud.unibas.ch",
    export=["PATH", "DOWNWARD_BENCHMARKS"],
)

exp = common_setup.IssueExperiment(
    # TODO: Adapt this path. It should probably be "../.." if you put this
    # script into experiments/something in the downward root directory (same
    # as the Downward Lab tutorial).
    REPO_DIR,
    revisions=REVISIONS,
    configs=CONFIGS,
    environment=ENVIRONMENT,
)

exp.add_suite(BENCHMARKS_DIR, SUITE)

exp.add_parser(exp.EXITCODE_PARSER)
exp.add_parser(exp.SINGLE_SEARCH_PARSER)
exp.add_parser(exp.PLANNER_PARSER)
exp.add_parser(PlateauParser())

entries = Attribute("max_entries_per_plateau", min_wins=False, function=arithmetic_mean, absolute=False)
depth = Attribute("max_depth", min_wins=False, function=arithmetic_mean, absolute=False)
width = Attribute("max_depth_width", min_wins=False, function=arithmetic_mean, absolute=False)
number_of_plateaus = Attribute("max_leveled_plateaus", min_wins=False, function=arithmetic_mean, absolute=False)
ATTRIBUTES = IssueExperiment.DEFAULT_TABLE_ATTRIBUTES + [entries, depth, width, number_of_plateaus]

exp.add_step("build", exp.build)
exp.add_step("start", exp.start_runs)
exp.add_step("parse", exp.parse)
exp.add_fetcher(name="fetch")
exp.add_report(AbsoluteReport(attributes=ATTRIBUTES))

exp.run_steps()
