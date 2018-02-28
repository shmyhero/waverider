import os
import json
from utils.iohelper import read_file_to_string, write_to_file
from common.pathmgr import PathMgr


class StrategyConfig(object):

    def __init__(self, strategy_name):
        self.name = strategy_name
        self.file_path = PathMgr.get_strategies_config_file(strategy_name)

    def get(self, section_name, key):
        if os.path.exists(self.file_path):
            try:
                content = read_file_to_string(self.file_path)
                json_data = json.loads(content)
                return json_data[section_name][key]
            except Exception as e:
                return None
        else:
            return None

    def set(self, section_name, key, value):
        dic = {}
        if os.path.exists(self.file_path):
            try:
                content = read_file_to_string(self.file_path)
                dic = json.loads(content)
            except Exception as e:
                pass
        if section_name in dic.keys():
            dic[section_name][key] = value
        else:
            section_dic = {key:value}
            dic[section_name] = section_dic
        write_to_file(self.file_path, json.dumps(dic))


if __name__ == '__main__':
    config = StrategyConfig('a')
    print config.get('spy', 'crash')
    config.set('spy', 'crash', True)
    config.set('spy', 'stop_order_price', 250)
    print config.get('spy', 'crash')
    print config.get('spy', 'stop_order_price')