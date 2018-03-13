import os
from utils.iohelper import ensure_dir_exists


class PathMgr(object):

    def __init__(self):
        pass

    @staticmethod
    def get_project_path():
        path_dir = os.path.dirname(os.path.abspath(__file__))
        return path_dir[:path_dir.rindex(os.path.sep)]

    @staticmethod
    def get_config_path():
        project_path = PathMgr.get_project_path()
        return os.path.join(project_path, 'config.conf')

    @staticmethod
    def get_log_path(sub_path=None):
        project_path = PathMgr.get_project_path()
        if sub_path:
            log_path = os.path.join(project_path, 'logs', sub_path)
        else:
            log_path = os.path.join(project_path, 'logs')
        ensure_dir_exists(log_path)
        return log_path

    @staticmethod
    def get_command_file_path(cmd_name):
        project_path = PathMgr.get_project_path()
        return os.path.join(project_path, 'ibbasic', 'commands',  cmd_name + '.py')

    @staticmethod
    def get_data_file_path(filename):
        project_path = PathMgr.get_project_path()
        return os.path.join(project_path, 'data', filename)

    @staticmethod
    def get_strategies_config_file(strategy_name):
        project_path = PathMgr.get_project_path()
        return os.path.join(project_path, 'strategies', 'configs', '%s.json' % strategy_name)

    @staticmethod
    def get_strategies_tradetrace_file(strategy_name):
        project_path = PathMgr.get_project_path()
        return os.path.join(project_path, 'strategies', 'tradetrace', '%s.csv' % strategy_name)

    @staticmethod
    def get_strategies_portfolio_file(strategy_name):
        project_path = PathMgr.get_project_path()
        return os.path.join(project_path, 'strategies', 'portfolio', '%s.csv' % strategy_name)



