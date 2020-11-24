import logging

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"
UNDERLINE_SEQ = "\033[04m"

YELLOW = '\033[93m'
WHITE = '\33[37m'
BLUE = '\033[34m'
LIGHT_BLUE = '\033[94m'
RED = '\033[91m'
GREY = '\33[90m'

KEYWORD_COLORS = {
    'WARNING': YELLOW,
    'INFO': LIGHT_BLUE,
    'DEBUG': WHITE,
    'CRITICAL': YELLOW,
    'ERROR': RED,
    'TRADE': '\33[102m\33[30m'
}

def formatter_message(message, use_color = True):
  if use_color:
      message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
  else:
      message = message.replace("$RESET", "").replace("$BOLD", "")
  return message

def format_word(message, word, color_seq, bold=False, underline=False):
    replacer = color_seq + word + RESET_SEQ
    if underline:
        replacer = UNDERLINE_SEQ + replacer
    if bold:
        replacer = BOLD_SEQ + replacer
    return message.replace(word, replacer)

class Formatter(logging.Formatter):
  '''
  This Formatted simply colors in the levelname i.e 'INFO', 'DEBUG'
  '''
  def __init__(self, msg, use_color = True):
    logging.Formatter.__init__(self, msg)
    self.use_color = use_color

  def format(self, record):
    levelname = record.levelname
    if self.use_color and levelname in KEYWORD_COLORS:
        levelname_color = KEYWORD_COLORS[levelname] + levelname + RESET_SEQ
        record.levelname = levelname_color
    record.name = GREY + record.name + RESET_SEQ
    return logging.Formatter.format(self, record)

class CustomLogger(logging.Logger):
    '''
    This adds extra logging functions such as logger.trade and also
    sets the logger to use the custom formatter
    '''
    FORMAT = "[$BOLD%(name)s$RESET] [%(levelname)s] %(message)s"
    COLOR_FORMAT = formatter_message(FORMAT, True)
    TRADE = 50
    POSITION = 49

    def __init__(self, name, logLevel='DEBUG'):
        logging.Logger.__init__(self, name, logLevel)                
        color_formatter = Formatter(self.COLOR_FORMAT)
        console = logging.StreamHandler()
        console.setFormatter(color_formatter)
        self.addHandler(console)
        logging.addLevelName(self.TRADE, "TRADE")
        logging.addLevelName(self.POSITION, "POS_STATUS")
        return

    def trade(self, message, *args, **kws):
        if self.isEnabledFor(self.TRADE):
            message = format_word(message, 'CLOSED ', YELLOW, bold=True)
            message = format_word(message, 'OPENED ', LIGHT_BLUE, bold=True)
            message = format_word(message, 'UPDATED ', BLUE, bold=True)
            message = format_word(message, 'CLOSED_ALL ', RED, bold=True)
            self._log(self.TRADE, message, args, **kws)

    def position(self, pos, *args, **kwargs):
        if self.isEnabledFor(self.POSITION):
            p_l = pos.profit_loss - pos.total_fees
            state = "OPEN" if pos.is_open() else "CLOSED"
            message = "Symbol {} | Amount_filled {} | State {} | Orders {}\n".format(
                pos.symbol, pos.amount, state, len(pos.orders))
            message += "\t\t\t  Net P/L {} | Gross P/L {} | Vol {} | Fees {}".format(
                p_l, pos.profit_loss, pos.volume, pos.total_fees)
            self._log(self.POSITION, message, args, **kwargs)

