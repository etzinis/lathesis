"""!
\brief Translate whole tex file

@author Efthymios Tzinis {etzinis@gmail.com}
"""

import argparse
import numpy as np
from googletrans import Translator
import line_translator


class LatexTranslator(object):

    def __init__(self, path, language):
        self.path = path
        self.language = language

    def skip_part_begin_end(self, lines, i, part):
        counter = i
        while counter < len(lines):
            if lines[counter].startswith('\\end{'+part+'}'):
                return counter + 1
            counter += 1

    def get_begin_end_part(self, line, parts_to_skip):
        for part in parts_to_skip:
            if line.startswith('\\begin{' + part):
                return part
        return None

    def translate_inside_list(self, lines, start_i, end_i, translator):
        for i in np.arange(start_i, end_i):
            if lines[i].startswith('\\item '):
                text = lines[i].split('\\item ')[-1]
                trans_text = line_translator.translate_line(text, '')

    def translate_latex(self):
        translator = Translator()

        with open(self.path) as f:
            lines = f.readlines()

        parts_to_skip = ['equation', 'array', 'figure', 'algorithm',
                         'hyp', 'thm', 'table', 'tabular']

        translated_lines = lines
        i = 0
        while i < len(translated_lines):
            this_line = translated_lines[i]

            # check lines for parts to skip
            part = self.get_begin_end_part(this_line, parts_to_skip)
            if part is not None:
                i = self.skip_part_begin_end(lines, i, part)
                continue

            # special translation for itemize and enumerate
            part = self.get_begin_end_part(this_line, ['itemize',
                                                       'enumerate'])
            if part is not None:
                start_i = i
                end_i = self.skip_part_begin_end(lines, i, part)

            i += 1

        return translated_lines


def get_args():
    """! Command line parser for translating text file """
    parser = argparse.ArgumentParser(
        description='Command line parser for translating latex file' )
    parser.add_argument("-i", "--input_tex", type=str,
        help="""Path where a tex file is located""",
        required=True)
    parser.add_argument("-l", "--language", type=str,
                        help="""Language to translate to""",
                        default='el',
                        choices=["af", "sq", "ar","be", "bg", "ca",
                                 "zh-CN", "zh-TW", "hr",
                                 "cs", "da", "nl", "en", "et", "tl",
                                 "fi", "fr", "gl", "de",
                                 "el", "iw", "hi", "hu", "is", "id",
                                 "ga", "it", "ja", "ko",
                                 "lv", "lt", "mk", "ms", "mt", "no",
                                 "fa", "pl", "pt", "ro",
                                 "ru", "sr", "sk", "sl", "es", "sw",
                                 "sv", "th", "tr", "uk",
                                 "vi", "cy", "yi"])
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()
    latex_translator = LatexTranslator(args.input_tex, args.language)
    translated_tex = latex_translator.translate_latex()