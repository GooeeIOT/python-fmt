import argparse
import math
import textwrap
from typing import Mapping

HELP_WIDTH = 55


def round_up_to(x: int, base: int) -> int:
    """Round ``x`` up to the nearest multiple of ``base``."""
    return int(math.ceil(x / base)) * base


class FormattedHelpArgumentParser(argparse.ArgumentParser):
    """Custom ArgumentParser that adds formatting to help text.

    Adds the following behavior to ``argparse.ArgumentParser``:

    - Uses ``argparse.RawTextHelpFormatter`` by default, but still wraps help text to 79 chars.
    - Automatically adds information about argument defaults to help text.
    - Generates custom help text for arguments with ``choices``.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("formatter_class", argparse.RawTextHelpFormatter)
        super().__init__(*args, **kwargs)

    def _fill(self, text: str, width=HELP_WIDTH, **kwargs):
        """Calls ``textwrap.fill`` with a default width of ``HELP_WIDTH``."""
        return textwrap.fill(text, width=width, **kwargs)

    def add_argument(self, *name_or_flags: str, **kwargs):
        """Wrap ``help`` text since we're using ``argparse.RawTextHelpFormatter``."""
        help_text = kwargs.get("help")
        if help_text:
            # Add default to help text if given and not already in help text.
            default = kwargs.get("default")
            if default and default is not argparse.SUPPRESS and "%(default)" not in help_text:
                help_text += " (default: %(default)s)"
            # Wrap help text.
            kwargs["help"] = self._fill(help_text)
        return super().add_argument(*name_or_flags, **kwargs)

    def add_choices_argument(self, *name_or_flags: str, choices: Mapping[str, str], **kwargs):
        """Add an argument with ``choices``.

        The ``choices`` param takes a mapping of choices to help text for each choice, and appends
        a formatted line to the given ``help`` for each choice.

        Note that this will not work if ``formatter_class`` is set to anything other than
        ``argparse.RawTextHelpFormatter`` (the default).
        """
        choices = dict(choices)

        # If ``default`` given, prepend "(default) " to the help text of the default choice.
        default = kwargs.get("default")
        if default and default is not argparse.SUPPRESS and default in choices:
            choices[default] = f"(default) {choices[default]}"

        # Generate help text for choices.
        prefix = "> "
        max_choice_len = max(len(choice) for choice in choices.keys()) + 1
        choice_width = round_up_to(max_choice_len, 2)
        choice_help_width = HELP_WIDTH - choice_width - len(prefix)
        choice_help_indent = " " * (choice_width + len(prefix))
        choice_fmt = "{prefix}{choice:<%d}{help:<%d}" % (choice_width, choice_help_width)
        choices_help = "\n".join(
            choice_fmt.format(
                prefix=prefix,
                choice=choice,
                help=self._fill(
                    text, width=choice_help_width, subsequent_indent=choice_help_indent
                ),
            )
            for choice, text in choices.items()
        )

        # Format final help text.
        help_text = "{}:\n\n{}".format(
            self._fill(kwargs.pop("help", "choices").rstrip(",.:;")), choices_help
        )
        return super().add_argument(*name_or_flags, choices=choices, help=help_text, **kwargs)
