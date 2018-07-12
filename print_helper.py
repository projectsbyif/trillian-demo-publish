import textwrap
from termcolor import colored, cprint


class Print():
    TICK = colored('✓', 'green', attrs=['bold'])
    CROSS = colored('x', 'red', attrs=['bold'])
    BULLET = colored('*', 'yellow', attrs=[])

    @staticmethod
    def status(text):
        cprint('\n{}\n'.format(text), 'yellow', attrs=['bold'])

    @staticmethod
    def tick(text, indent=2):
        indented = Print.indent(
            '{} {}'.format(Print.TICK, text),
            indent
        )

        cprint(indented)

    @staticmethod
    def bullet(text, indent=2):
        indented = Print.indent(
            '{} {}'.format(Print.BULLET, text),
            indent
        )

        cprint(indented)

    @staticmethod
    def cross(text, indent=2):
        indented = Print.indent(
            '{} {}'.format(Print.CROSS, text),
            indent
        )

        cprint(indented)

    @staticmethod
    def normal(text, indent=2):
        cprint(Print.indent(text, indent))

    @staticmethod
    def indent(text, number_of_spaces):
        return textwrap.indent(text, ' ' * number_of_spaces)
