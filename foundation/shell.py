# coding=utf-8
import subprocess
import shlex


class Shell(object):
    @classmethod
    def run(cls, cmd):
        if cmd is None or len(cmd) < 1:
            return None
        output, error = subprocess.Popen(
            shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1
        ).communicate()
        return {
            "output": output.decode('utf-8'),
            "error": error.decode('utf-8'),
        }
