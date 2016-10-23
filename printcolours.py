BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
END = '\033[0m'


def _colour_seq(colour, text):
    return colour + text + END


def yellow(text):
    return _colour_seq(YELLOW, text)


def red(text):
    return _colour_seq(RED, text)


def blue(text):
    return _colour_seq(BLUE, text)


def green(text):
    return _colour_seq(GREEN, text)
