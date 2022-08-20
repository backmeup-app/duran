from flask import current_app, render_template
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
            requests.post(
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
        except Exception:
            exception = sys.exc_info()
            print(exception)
