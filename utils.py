import json
import os
from os.path import expanduser
from typing import Dict
from typing import Optional

from PyInquirer import prompt


def is_configured() -> bool:
    if not os.path.isdir(os.path.join(os.path.expanduser('~'), '.aws_helper')):
        return False
    elif not os.path.isfile(
        os.path.join(
            os.path.expanduser('~'),
            '.aws_helper', 'credentials.json',
        ),
    ):
        return False
    else:
        return True


def configure_aws_helper(argv: Optional[Dict[str, str]] = None) -> None:

    questions = [
        {
            'type': 'input',
            'name': 'access_key',
            'message': 'AWS Access Key ID',
        },
        {
            'type': 'input',
            'name': 'secret_key',
            'message': 'AWS Secret Access Key',
        },
        {
            'type': 'input',
            'name': 'region',
            'message': 'Default region name',
        },
        {
            'type': 'input',
            'name': 'output_fmt',
            'message': 'Default output format',
        },
    ]

    home = expanduser('~')
    helper_path = os.path.join(home, '.aws_helper')
    fpath = os.path.join(helper_path, 'credentials.json')

    # write_perm = os.access(fpath, os.W_OK)  # Check for write access
    write_perm = os.access(helper_path, os.W_OK)  # Check for write access
    if (write_perm):
        answers = prompt(
            questions, keyboard_interrupt_msg='Aborted!',
        ) if argv is None else argv
        for key, value in answers.items():
            if len(value) == 0:
                answers[key] = None
        if not os.path.isdir(helper_path):
            os.mkdir(helper_path)
        with open(fpath, 'w+') as f:
            json.dump(answers, f)
    else:
        raise PermissionError(
            'Tool doesnot have permission to save credentials. Make sure you have appropriate permissions',
        )
