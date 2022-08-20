from flask import render_template
from utilities.exception import log_exception
from os import environ
import requests
import sys


class Mail:
    def __init__(self, email: str, subject: str, template: str, **kwargs):
        self.email = email
        self.subject = subject
        self.template = template
        self.args = kwargs

    def send(self):
        try:
            response = requests.post(
                environ.get("MAIL_BASE_URL"),
                auth=("api", environ.get("MAIL_API_KEY")),
                data={
                    "from": "{0} {1}".format(
                        environ.get("MAIL_FROM"), environ.get("MAIL_FROM_URL")
                    ),
                    "to": [self.email],
                    "subject": self.subject,
                    "html": render_template(self.template, **self.args),
                },
            )

            if response.status_code != 200:
                raise Exception("Mail notification failed")
        except Exception:
            exception = sys.exc_info()
            log_exception(exception)
