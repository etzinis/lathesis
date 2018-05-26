"""!
\brief Translate a line from Latex_code

@author Efthymios Tzinis {etzinis@gmail.com}
"""

from googletrans import Translator
import re
import argparse
import numpy as np


def get_args():
    """! Command line parser for extracting """
    parser = argparse.ArgumentParser(
        description='Line Translator' )
    parser.add_argument("-i", "--input_text",
                        type=str,
                        help="""Input string to translate""",
                        required=True)
    parser.add_argument("-lang", "--language",
                        type=str,
                        help="""Language to translate this text""",
                        default='el')
    args = parser.parse_args()
    return args


def remove_spaces_for_references_and_citations(line):

    refined_line = line
    for command in ['ref', 'cite']:
        command_string = "\\"+command+"{"
        ref_inlines = refined_line.split(command_string)
        if len(ref_inlines) > 1:
            for i in np.arange(1, len(ref_inlines)):
                closure_ind = ref_inlines[i].index('}')
                ref_inlines[i] = (ref_inlines[i][:closure_ind].replace(
                                ' ', '') + ref_inlines[i][closure_ind:])
            refined_line = command_string.join(ref_inlines)
    return refined_line


def refine_latex_translation(new_line):
    refined_line = new_line
    ref_commands = ['ref', 'cite', 'footnote', 'label', 'section',
                    'subsection', 'subsubsection', 'caption']
    for com in ref_commands:
        refined_line = re.sub("\\ "+com+" {", com+"{", refined_line)

    # supress all produced spaces for inline math code, references
    # and citations

    math_inline = refined_line.split("$")
    for i in np.arange(1, len(math_inline)-1, 2):
        math_inline[i] = math_inline[i].replace(' ', '')
    refined_line = '$'.join(math_inline)

    refined_line = remove_spaces_for_references_and_citations(
                   refined_line)

    return refined_line


def translate_line(text, language):
    trans = Translator()
    try:
        translated_text = trans.translate(text, language).text
    except Exception as e:
        translated_text = None
        print e
        print 'Skipping...'

    print '\n'
    print translated_text

    refined_text = refine_latex_translation(translated_text)

    print '\n'
    print '~'*20
    print refined_text

if __name__ == "__main__":
    args = get_args()
    translate_line(args.input_text, args.language)