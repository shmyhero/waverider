import os

class Shell:
    """ This class encapsulte all the shell command line and utilities to functions.
    """

    # run shell command, it return_p is True, the output will be returned
    @staticmethod
    def run_cmd(cmd, return_p=False):
        if return_p:
            r = os.popen(cmd)
            text = r.read()
            r.close()
            return text
            # p = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # text = p.stdout.read()
            # return text
        else:
            os.system(cmd)
