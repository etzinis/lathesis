"""!
\brief Translate whole tex file

@author Efthymios Tzinis {etzinis@gmail.com}
"""

import argparse
import numpy as np


def get_args():
    """! Command line parser for translating text file """
    parser = argparse.ArgumentParser(
        description='Command line parser for translating latex file' )
    parser.add_argument("-i", "--input_tex", type=str,
        help="""Path where a tex file is located""",
        required=True)
    args = parser.parse_args()
    return args


def skip_part_begin_end(lines, i, part):
    counter = i
    while counter < len(lines):
        if lines[counter].startswith('\\end{'+part+'}'):
            return counter + 1
        counter += 1


def get_begin_end_part(line, parts_to_skip):
    for part in parts_to_skip:
        if line.startswith('\\begin{' + part):
            return part
    return None


def tr


def translate_latex(path):
    with open(path) as f:
        lines = f.readlines()

    parts_to_skip = ['equation', 'array', 'figure', 'algorithm',
                     'hyp', 'thm', 'table', 'tabular']

    translated_lines = lines
    i = 0
    while i < len(translated_lines):
        this_line = translated_lines[i]

        # check lines for parts to skip
        part = get_begin_end_part(this_line, parts_to_skip)
        if part is not None:
            i = skip_part_begin_end(lines, i, part)
            continue

        # special translation for itemize and enumerate
        part = get_begin_end_part(this_line, ['itemize', 'enumerate'])
        if part is not None:
            start_i = i
            end_i = skip_part_begin_end(lines, i, part)
            for i in np.arange(start_i, end_i):
                print lines[i]





        i += 1



    return translated_lines


if __name__ == "__main__":
    args = get_args()
    translated_tex = translate_latex(args.input_tex)