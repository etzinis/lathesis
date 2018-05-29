"""!
\brief Translate a line from Latex_code

@author Efthymios Tzinis {etzinis@gmail.com}
"""

from googletrans import Translator
import re
import argparse
import numpy as np

encoder = dict([(x, ''.join([str(n)+x[n] for n in np.arange(len(x))]))
                for x in ['math', 'cite', 'ref', 'url']])

decoder = {}
for k, v in encoder.items():
    decoder[v] = k

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
    for command in ['ref', 'cite', 'Ref', 'Cite']:
        command_string = "\\"+command+"{"
        ref_inlines = refined_line.split(command_string)
        if len(ref_inlines) > 1:
            for i in np.arange(1, len(ref_inlines)):
                closure_ind = ref_inlines[i].index('}')
                ref_inlines[i] = (ref_inlines[i][:closure_ind].replace(
                                ' ', '') + ref_inlines[i][closure_ind:])
            refined_line = command_string.lower().join(ref_inlines)
    return refined_line


def refine_latex_translation(new_line):
    refined_line = new_line
    ref_commands = ['ref', 'cite', 'footnote', 'label', 'section',
                    'subsection', 'subsubsection', 'caption',
                    'textit', 'textbf', 'em', 'Ref']
    for com in ref_commands:
        refined_line = re.sub("\\ "+com+" {", com+"{", refined_line)

    # supress all produced spaces for inline math code, references
    # and citations

    math_inline = refined_line.split("$")
    for i in np.arange(1, len(math_inline), 2):
        math_inline[i] = math_inline[i].replace(' ', '')
    refined_line = '$'.join(math_inline)

    refined_line = remove_spaces_for_references_and_citations(
                   refined_line)

    return refined_line


def encode_command(text, command):
    initial_commands = []
    encoded_text = text

    command_string = "\\" + command + "{"
    command_inlines = text.split(command_string)
    if len(command_inlines) > 1:
        encoded_text = command_inlines[0]

        for i in np.arange(1, len(command_inlines)):
            string_to_be_closed = command_inlines[i]
            cnt = 1
            closure_index = 0
            for j, ch in enumerate(string_to_be_closed):
                if ch == '{':
                    cnt += 1
                elif ch == '}':
                    cnt -= 1
                    if cnt == 0:
                        closure_index = j
                        break

            initial_commands.append(command_string +
                                    string_to_be_closed[:j+1])
            encoded_text += encoder[command] + string_to_be_closed[j+1:]

    return encoded_text, initial_commands



def encode_inline_latex(text):
    initial_commands = {}

    # encode inline math
    encoded_text = text

    initial_math = []
    math_inline = encoded_text.split("$")
    for i in np.arange(1, len(math_inline), 2):
        initial_math.append('$'+math_inline[i]+'$')
    encoded_text = encoder['math'].join(math_inline[::2])
    initial_commands['math'] = initial_math

    # encode all the other functions
    for command in ['cite', 'ref', 'url']:
        encoded_text, these_commands = encode_command(encoded_text,
                                                      command)
        initial_commands[command] = these_commands

    return encoded_text, initial_commands


def translate_line(text, language, translator=None):
    if translator is None:
        trans = Translator()
    else:
        trans = translator
    try:
        encoded_text, initial_commands = encode_inline_latex(text)
        translated_text = trans.translate(encoded_text, language).text
        # translated_text = trans.translate(text, language).text
        # refined_text = refine_latex_translation(translated_text)
    except Exception as e:
        translated_text = text
        print "Failed to translate: {}".format(text)
        print e
        print 'Skipping...'


    return translated_text

if __name__ == "__main__":
    args = get_args()
    trans_line = translate_line(args.input_text, args.language)
    print trans_line