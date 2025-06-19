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
        "f, h^-ff, <d>, fifo",
        [
            "--search",
            "let(h, lmcut(), let(hff, ff(transform=adapt_costs(one)), eager(div_tiebreaking([sum([g(), h]), hff], unsafe_pruning=false, tiebreaking_criteria=fifo), reopen_closed=true, f_eval=sum([g(), h]), use_depth=true)))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^-ff, <d>, lifo",
        [
            "--search",
            "let(h, lmcut(), let(hff, ff(transform=adapt_costs(one)), eager(div_tiebreaking([sum([g(), h]), hff], unsafe_pruning=false, tiebreaking_criteria=lifo), reopen_closed=true, f_eval=sum([g(), h]), use_depth=true)))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^-ff, <d>, ro1",
        [
            "--search",
            "let(h, lmcut(), let(hff, ff(transform=adapt_costs(one)), eager(div_tiebreaking([sum([g(), h]), hff], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h]), use_depth=true)))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^-ff, <d>, ro2",
        [
            "--search",
            "let(h2, lmcut(), let(hff2, ff(transform=adapt_costs(one)), eager(div_tiebreaking([sum([g(), h2]), hff2], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h2]), use_depth=true)))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^-ff, <d>, ro3",
        [
            "--search",
            "let(h3, lmcut(), let(hff3, ff(transform=adapt_costs(one)), eager(div_tiebreaking([sum([g(), h3]), hff3], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h3]), use_depth=true)))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^-ff, <d>, ro4",
        [
            "--search",
            "let(h4, lmcut(), let(hff4, ff(transform=adapt_costs(one)), eager(div_tiebreaking([sum([g(), h4]), hff4], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h4]), use_depth=true)))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^-ff, <d>, ro5",
        [
            "--search",
            "let(h5, lmcut(), let(hff5, ff(transform=adapt_costs(one)), eager(div_tiebreaking([sum([g(), h5]), hff5], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h5]), use_depth=true)))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^-ff, <d>, ro6",
        [
            "--search",
            "let(h6, lmcut(), let(hff6, ff(transform=adapt_costs(one)), eager(div_tiebreaking([sum([g(), h6]), hff6], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h6]), use_depth=true)))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^-ff, <d>, ro7",
        [
            "--search",
            "let(h7, lmcut(), let(hff7, ff(transform=adapt_costs(one)), eager(div_tiebreaking([sum([g(), h7]), hff7], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h7]), use_depth=true)))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^-ff, <d>, ro8",
        [
            "--search",
            "let(h8, lmcut(), let(hff8, ff(transform=adapt_costs(one)), eager(div_tiebreaking([sum([g(), h8]), hff8], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h8]), use_depth=true)))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^-ff, <d>, ro9",
        [
            "--search",
            "let(h9, lmcut(), let(hff9, ff(transform=adapt_costs(one)), eager(div_tiebreaking([sum([g(), h9]), hff9], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h9]), use_depth=true)))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "f, h^-ff, <d>, ro0",
        [
            "--search",
            "let(h0, lmcut(), let(hff0, ff(transform=adapt_costs(one)), eager(div_tiebreaking([sum([g(), h0]), hff0], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h0]), use_depth=true)))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    # TODO: Add your configs.
]

BENCHMARKS_DIR = os.environ["DOWNWARD_IPC_BENCHMARKS"]
REPO_DIR = os.environ["DOWNWARD_REPO"]

#if common_setup.is_test_run():
#    SUITE = common_setup.IssueExperiment.DEFAULT_TEST_SUITE
#    ENVIRONMENT = LocalEnvironment(processes=2)
#else:
SUITE = common_setup.DEFAULT_OPTIMAL_SUITE
ENVIRONMENT = BaselSlurmEnvironment(
    # Choose between infai_1 or infai_2. Either works but stick to a
    # single partition when results have to be comparable.
    partition="infai_2",
    # TODO: Change this to your own email, you will get notified when your
    # jobs finish.
    email="m.franco@stud.unibas.ch",
    export=["PATH", "DOWNWARD_IPC_BENCHMARKS"],
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
