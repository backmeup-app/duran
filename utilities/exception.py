from flask import current_app
import traceback


def log_exception(exception):
    stack_trace = " ".join(traceback.format_exception(*exception))
    current_app.logger.error("{0}\n{1}".format(exception[1], stack_trace))
