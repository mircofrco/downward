# TODO
# - Place this file in the same directory as the experiment script(s)
# - Adapt the patterns below and rename the parser class appropriately
# - Add the following lines to the experiment script(s):
#   from <name_of_this_file> import LandmarkParser
#   exp.add_pattern(LandmarkParser())
# - Define the relevant Attribute object(s) in the experiment script(s), e.g.
#   Attribute("lmgraph_generation_time", min_wins=False)
# - Add the Attribute object(s) to the list of attributes to be shown in the
#   report

import re

from lab.parser import Parser

PATTERNS = [
    ["lmgraph_generation_time", r"Landmark graph generation time: (.+)s", float],
    ["landmarks", r"Landmark graph contains (\d+) landmarks, of which \d+ are disjunctive, \d+ are conjunctive, and \d+ are derived.", int],
]

class LandmarkParser(Parser):
    def __init__(self):
        Parser.__init__(self)
        for name, pattern, typ in PATTERNS:
            self.add_pattern(name, pattern, type=typ)
