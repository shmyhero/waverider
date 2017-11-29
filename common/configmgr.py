import ConfigParser
from pathmgr import PathMgr


class ConfigMgr(dict):
    conf_dict = None

    @staticmethod
    def read_config():
        conf = ConfigParser.RawConfigParser()
        conf.read(PathMgr.get_config_path())
        return conf

    @staticmethod
    def get_config():
        if ConfigMgr.conf_dict is None:
            dic = {}
            conf = ConfigMgr.read_config()
            for section in conf.sections():
                section_dic = {}
                for option in conf.options(section):
                    section_dic[option] = conf.get(section, option)
                dic[section] = section_dic
            ConfigMgr.conf_dict = dic
        return ConfigMgr.conf_dict

    @staticmethod
    def get_ib_config():
        return ConfigMgr.get_config()['ib']

    @staticmethod
    def get_db_config():
        return ConfigMgr.get_config()['db']
