import sys
import logging
from colorlog import ColoredFormatter as ColoredFormatterBase
from colorlog.escape_codes import escape_codes
import sqlparse


class ColoredFormatter(ColoredFormatterBase):
    def format(self, record):
        msg = record.getMessage()
        exec_time = float(msg[:msg.index(' ')].replace('(', '').replace(')', ''))
        query_str = msg[msg.index(' ') + 1:msg.index('; args')]
        exec_time_name = 'FAST'

        if exec_time >= .5:
            exec_time_name = 'MEDIUM'
        if exec_time >= .1:
            exec_time_name = 'SLOW'

        separator = '*' * 80
        record.msg = '\n%s\n%s\n%s\n%s\n%s\n' % (
            separator,
            exec_time, '-' * 80,
            sqlparse.format(query_str, reindent=True).strip(),
            separator
        )

        if exec_time_name in self.log_colors:
            color = self.log_colors[exec_time_name]
            record.log_color = escape_codes[color]
        else:
            record.log_color = ""

        if sys.version_info > (2, 7):
            message = super(ColoredFormatterBase, self).format(record)
        else:
            message = logging.Formatter.format(self, record)

        if self.reset and not message.endswith(escape_codes['reset']):
            message += escape_codes['reset']

        return message

