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
        self.translator = Translator()
        with open(self.path) as f:
            self.lines = f.readlines()

        self.parts_to_skip = ['equation', 'array', 'figure',
                              'algorithm', 'hyp', 'thm', 'table',
                              'tabular']
        self.list_commands = ['itemize', 'enumerate']

    def skip_part_begin_end(self, i, part):
        counter = i
        while counter < len(self.lines):
            if self.lines[counter].startswith('\\end{' + part + '}'):
                return counter + 1
            counter += 1

    def get_begin_end_part(self, line, parts):
        for part in parts:
            if line.startswith('\\begin{' + part):
                return part
        return None

    def translate_inside_list(self, start_i, end_i):
        for i in np.arange(start_i, end_i):
            if self.lines[i].startswith('\\item '):
                text = self.lines[i].split('\\item ')[-1]
                trans_text = line_translator.translate_line(
                             text, self.language,
                             translator=self.translator)

                self.lines[i] = '\item ' + trans_text

    def remove_spaces_from_label_lines(self):
        for i in np.arange(len(self.lines)):
            if self.lines[i].startswith('\\label{'):
                print self.lines[i]
                self.lines[i] = self.lines[i].replace(' ', '')
                print self.lines[i]

    def translate_latex(self):
        # remove spaces from labels as they cause problem in later
        # process
        self.remove_spaces_from_label_lines()

        i = 0
        while i < len(self.lines):
            this_line = self.lines[i]

            # # check lines for parts to skip
            # part = self.get_begin_end_part(this_line,
            #                                self.parts_to_skip)
            # if part is not None:
            #     i = self.skip_part_begin_end(i, part)
            #     continue

            # # special translation for itemize and enumerate
            # part = self.get_begin_end_part(this_line,
            #                                self.list_commands)
            # if part is not None:
            #     start_i = i
            #     end_i = self.skip_part_begin_end(i, part) - 1
            #     self.translate_inside_list(start_i, end_i)
            #     i = end_i + 1
            #     continue

            # for special lines skip the translation
            if this_line.startswith('\\'):
                pass

            i += 1

        return self.lines


def get_args():
    """! Command line parser for translating text file """
    parser = argparse.ArgumentParser(
        description='Command line parser for translating latex file')
    parser.add_argument("-i", "--input_tex", type=str,
                        help="""Path where a tex file is located""",
                        required=True)
    parser.add_argument("-l", "--language", type=str,
                        help="""Language to translate to""",
                        default='el',
                        choices=["af", "sq", "ar", "be", "bg", "ca",
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
