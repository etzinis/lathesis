"""!
\brief Translate a line from Latex_code

@author Efthymios Tzinis {etzinis@gmail.com}
"""

from googletrans import Translator
import re
import argparse


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


def refine_latex_translation(new_line):
    refined_line = new_line
    ref_commands = ['ref', 'cite', 'footnote', 'label', 'section',
                    'subsection', 'subsubsection', 'caption']
    for com in ref_commands:
        refined_line = re.sub("\\ "+com+" {", com+"{", refined_line)

    # p = re.compile("\$[.+\$")
    # a = p.match(refined_line)
    refined_line = re.findall("\$.+\$", refined_line)
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
    print refined_text

if __name__ == "__main__":
    args = get_args()
    translate_line(args.input_text, args.language)