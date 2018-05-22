"""!
\brief Extract Abbreviations List from tex file

@author Efthymios Tzinis {etzinis@gmail.com}
"""

import argparse
import re


def get_args():
    """! Command line parser for extracting """
    parser = argparse.ArgumentParser(
        description='Utterance level classification Leave one '
                    'speaker out schema pipeline' )
    parser.add_argument("-i", "--input_tex", type=str,
        help="""Path where a tex file is located""",
        required=True)
    args = parser.parse_args()
    return args


def spot_abbreviations(path):

    abbreviations = {}

    with open(path) as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        possible_abbreviations = re.findall(' \([A-Z]+[s]*\)', line)
        trimmed_line = re.sub('[:{}()\.,]', '', line)
        trimmed_line = re.sub('\\\\textit', '', trimmed_line)
        words = trimmed_line.split(' -')

        for a in possible_abbreviations:
            capitals = ''.join([c for c in a if c.isupper()])
            index = line.index(a)
            abbreviations[a] = line[max(index - 50, 0) :
                                    min(index + 50, len(line))]

    return abbreviations

def get_abbreviations(path):
    abbreviations = spot_abbreviations(path)
    for a in sorted(abbreviations.keys()):
        print "{}: {}".format(a, abbreviations[a])

if __name__ == "__main__":
    args = get_args()
    abbreviations = get_abbreviations(args.input_tex)