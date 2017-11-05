class PyColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def colorize_log(log_level, msg, should_colorize=True):
    """
    Returns a colored string to log
    :param should_colorize: boolean that specifies if the log is to be colorized
    :param log_level: level of message to logged
    :param msg: message to be logged
    :return:
    """
    colorize_log_dict = {
        "NORMAL": PyColors.ENDC,
        "WARNING": PyColors.WARNING,
        "SUCCESS": PyColors.OKGREEN,
        "FAIL": PyColors.FAIL,
        "RESET": PyColors.ENDC
    }

    if should_colorize:
        if log_level in colorize_log_dict:
            return colorize_log_dict[str(log_level)] + msg + colorize_log_dict['RESET']
        return colorize_log_dict["NORMAL"] + msg + colorize_log_dict["RESET"]
    return msg