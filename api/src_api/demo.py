from typing import Tuple
from flask import Flask, request, abort
import logging
from logging.config import dictConfig
import yaml
import asyncio


with open('src_api/logging.yml') as f:
    dictConfig(yaml.safe_load(f))
log = logging.getLogger()

api = Flask(__name__)


@api.route('/')
def hello():
    return "See API documentation: TBD", 200


@api.route('/command', methods=['PUT'])
def command():
    """tbd"""
    req_json = request.get_json()
    # check if `command` is a key in the request body
    if 'command' not in req_json:
        abort(400)

    # handle command
    status, out, err = run_command(req_json['command'])

    return {"status": status, "stdout": out, "stderr": err}, 200


def run_command(command_string: str) -> Tuple[int, str, str]:
    """Run the command in command_string"""
    log.info('command string: %s', command_string)

    # rc, out, err = basic_run_command(command_string)
    rc, out, err = asyncio.run(async_run_command(command_string))

    log.info('Return Code: %s', rc)
    log.info('output is: %s', out)
    log.info('error is: %s', err)

    status = -1 if err else 0

    return status, out, err


def basic_run_command(command_string: str) -> Tuple[int, str, str]:
    """Run the command synchronously"""
    import subprocess

    result = subprocess.run(command_string,
                            capture_output=True,
                            check=True,
                            shell=True
                            )

    return result.returncode, result.stdout.decode(), result.stderr.decode()


async def async_run_command(command_string: str) -> Tuple[int, str, str]:
    """Run the command asynchronously"""
    proc = await asyncio.create_subprocess_shell(
        command_string,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()

    return proc.returncode, stdout.decode(), stderr.decode()


if __name__ == "__main__":
    api.run(host='0.0.0.0', port=5000, debug=True)
