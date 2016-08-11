# coding=utf-8
from fancyladder import ladder
from jinja2 import Environment, FileSystemLoader
import os


class Surge(ladder.Ladder):
    def __init__(self):
        super(Surge, self).__init__()
        self._id = 'surge'

    def id(self):
        return self._id

    def gen(self, **kwargs):
        rule_path = kwargs['rule_path']
        template_path = os.path.join(rule_path, self._id)

        env = Environment(loader=FileSystemLoader(template_path), trim_blocks=True)

        context = {
            'gfwlist': kwargs['gfwlist_proxy_domain'],
            'user_rule': kwargs['user_proxy_domain'],
        }

        rendered = env.get_template('surge.conf').render(**context)
        return {
            'surge.conf': rendered
        }
