#! /usr/bin/env python
# -*- coding: utf-8 -*-

import common_setup
from common_setup import IssueConfig, IssueExperiment

import os

from lab.reports import Attribute
from lab.reports import arithmetic_mean

from downward.reports.absolute import AbsoluteReport

from lab.environments import LocalEnvironment, BaselSlurmEnvironment
from experiment-parser import PlateauParser

# TODO: Enter git commit hash of code version you want to use.
REVISIONS = ["1a415eebfdd9640db81d4458f7bfed8ab1ddd7a5"]
DRIVER_OPTIONS = ["--overall-time-limit", "5m"]
CONFIGS = [
    common_setup.IssueConfig(
        "[f, h^, fifo]",
        [
            "--search",
            "let(h, lmcut(), let(h_adapted, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h]), h_adapted], unsafe_pruning=false, tiebreaking_criteria=fifo), reopen_closed=true, f_eval=sum([g(), h]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "[f, h^, lifo]",
        [
            "--search",
            "let(h, lmcut(), let(h_adapted, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h]), h_adapted], unsafe_pruning=false, tiebreaking_criteria=lifo), reopen_closed=true, f_eval=sum([g(), h]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "[f, h^, ro]",
        [
            "--search",
            "let(h, lmcut(), let(h_adapted, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h]), h_adapted], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "[f, h, h^, fifo]",
        [
            "--search",
            "let(h, lmcut(), let(h_adapted, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h]), h, h_adapted], unsafe_pruning=false, tiebreaking_criteria=fifo), reopen_closed=true, f_eval=sum([g(), h]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "[f, h, h^, lifo]",
        [
            "--search",
            "let(h, lmcut(), let(h_adapted, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h]), h, h_adapted], unsafe_pruning=false, tiebreaking_criteria=lifo), reopen_closed=true, f_eval=sum([g(), h]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "[f, h, <d>, ro]",
        [
            "--search",
            "let(h, lmcut(), let(h_adapted, lmcut(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h]), h, h_adapted], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "[f, h^-ff, fifo]:",
        [
            "--search",
            "let(h, lmcut(), let(hff, ff(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h]), hff], unsafe_pruning=false, tiebreaking_criteria=fifo), reopen_closed=true, f_eval=sum([g(), h]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "[f, h^-ff, lifo]:",
        [
            "--search",
            "let(h, lmcut(), let(hff, ff(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h]), hff], unsafe_pruning=false, tiebreaking_criteria=lifo), reopen_closed=true, f_eval=sum([g(), h]))))",
        ],
        driver_options=DRIVER_OPTIONS,
    ),
    common_setup.IssueConfig(
        "[f, h^-ff, ro]:",
        [
            "--search",
            "let(h, lmcut(), let(hff, ff(transform=adapt_costs(one)), eager(criteria_tiebreaking([sum([g(), h]), hff], unsafe_pruning=false, tiebreaking_criteria=random), reopen_closed=true, f_eval=sum([g(), h]))))",
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
exp.add_pattern(PlateauParser())

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
