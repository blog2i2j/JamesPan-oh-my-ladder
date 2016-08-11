# coding=utf-8
import os

DEFAULT_PLUGIN_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'plugins')
DEFAULT_RULE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rules')
GFW_LIST_URL = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
GFW_LIST_FILE = 'gfwlist.txt'
GFW_LIST_ARCHIVE = 'gfwlist-%s.txt'
