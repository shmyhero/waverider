from utils.logger import Logger
from common.pathmgr import PathMgr


def symbol(asset):
    return asset


def symbols(*args):
    return list(args)


log = Logger(__name__, PathMgr.get_log_path())
