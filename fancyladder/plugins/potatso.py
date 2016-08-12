# coding=utf-8
from fancyladder import ladder
from jinja2 import Environment, FileSystemLoader
import os


class Potatso(ladder.Ladder):
    def __init__(self):
        super(Potatso, self).__init__()
        self._id = 'potatso'

    def id(self):
        return self._id

    def gen(self, **kwargs):
        rule_path = kwargs['rule_path']
        template_path = os.path.join(rule_path, self._id)

        env = Environment(loader=FileSystemLoader(template_path), trim_blocks=True)

        with open(os.path.join(template_path, 'rule-reject.txt')) as f:
            lines = map(str.strip, f.readlines())

        context = {
            'gfwlist': kwargs['gfwlist_proxy_domain'],
            'user_rule': kwargs['user_proxy_domain'],
            'rule_reject': lines
        }

        rendered = env.get_template('potatso.conf').render(**context)

        return {
            'potatso.conf': rendered
        }
