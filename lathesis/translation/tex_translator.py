"""!
\brief Translate whole tex file

@author Efthymios Tzinis {etzinis@gmail.com}
"""

import argparse
import numpy as np
from googletrans import Translator
import line_translator
import os
from progress.bar import ChargingBar


class LatexTranslator(object):

    def __init__(self, path, language, outpath=None):
        self.path = path
        self.language = language
        self.translator = Translator()
        with open(self.path) as f:
            self.lines = f.readlines()

        self.parts_to_skip = ['equation', 'array', 'figure',
                              'algorithm', 'hyp', 'thm', 'table',
                              'tabular']
        self.list_commands = ['itemize', 'enumerate']
        self.outpath = outpath
        self.bar = ChargingBar('Translating Tex File...',
                               max=len(self.lines))

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
                self.lines[i] = self.lines[i].replace(' ', '')

    def save_to_file(self):
        if self.outpath is not None:
            try:
                if not os.path.isdir(os.path.dirname(self.outpath)):
                    os.makedirs(os.path.dirname(self.outpath))
            except Exception as e:
                print "Failed to create directories: {}".format(
                    os.path.dirname(self.outpath)
                )
                print e

            try:
                fo = open(self.outpath, 'wb')
                for i in np.arange(len(self.lines)):
                    fo.write(self.lines[i])
                fo.close()

            except Exception as e:
                print "Failed to save translated tex in: {}".format(
                    self.outpath
                )
                print e

    def translate_latex(self):
        # remove spaces from labels as they cause problem in later
        # process
        self.remove_spaces_from_label_lines()

        i = 0
        prev = i
        while i < len(self.lines):
            for j in np.arange(i - prev):
                self.bar.next()
                prev = i
            this_line = self.lines[i]

            # check lines for parts to skip
            part = self.get_begin_end_part(this_line,
                                           self.parts_to_skip)
            if part is not None:
                i = self.skip_part_begin_end(i, part)
                continue

            # special translation for itemize and enumerate
            part = self.get_begin_end_part(this_line,
                                           self.list_commands)
            if part is not None:
                start_i = i
                end_i = self.skip_part_begin_end(i, part) - 1
                self.translate_inside_list(start_i, end_i)
                i = end_i + 1
                continue

            # for special lines skip the translation
            if this_line.startswith('\\') or this_line.startswith('%'):
                i += 1
                continue

            # text lines should be translated normally only if they
            # are not empty
            if len(this_line) > 3:
                self.lines[i] = line_translator.translate_line(
                                self.lines[i], self.language,
                                translator=self.translator)

            i += 1

        # translate captions as well
        for i in np.arange(len(self.lines)):
            if '\caption' in self.lines[i]:
                before, text = self.lines[i].split('\caption{')
                self.lines[i] = before + '\caption{' + \
                                line_translator.translate_line(
                                text, self.language,
                                translator=self.translator)

        self.bar.finish()

        self.save_to_file()
        for i in np.arange(len(self.lines)):
            print self.lines[i].split("\n")[0]

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
    parser.add_argument("-o", "--output_tex", type=str,
                        help="""Path where the translated tex file 
                        will be created. If the directory does not 
                        exists it will be automatically created.""",
                        default='/tmp/translated_texfile.tex')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()
    latex_translator = LatexTranslator(args.input_tex,
                                       args.language,
                                       outpath=args.output_tex)
    translated_tex = latex_translator.translate_latex()
