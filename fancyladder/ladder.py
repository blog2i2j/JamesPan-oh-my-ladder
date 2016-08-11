# coding=utf-8
import abc
from yapsy.IPlugin import IPlugin


class LadderException(Exception):
    pass


class Ladder(IPlugin):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def id(self):
        """identify for ladder"""
        pass

    @abc.abstractmethod
    def gen(self, **kwargs):
        """

        :param kwargs: rule_path, plugin_path, gfwlist_proxy_domain, user_proxy_domain
        :return:
        """
        pass
