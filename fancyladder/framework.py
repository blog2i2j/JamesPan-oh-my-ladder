# coding=utf-8
import os
import sys
import common
import base64


class LadderFramework(object):
    def __init__(self, rule_path, plugin_path):
        self.rule_path = rule_path
        self.plugin_path = plugin_path

    def run(self, expect_ladder):
        from yapsy.PluginManager import PluginManager
        from fancyladder.ladder import Ladder, LadderException
        from contrib.gfwlist2pac import parse_gfwlist, reduce_domains

        mgr = PluginManager()
        mgr.setPluginPlaces(self.plugin_path)
        mgr.collectPlugins()

        supported = []
        for plugin in mgr.getAllPlugins():
            candidate = plugin.plugin_object
            if not isinstance(candidate, Ladder):
                continue
            if expect_ladder == candidate.id():
                ladder_ins = candidate
                break
            else:
                supported.append(candidate.id())
        else:
            raise LadderException(
                'ladder %s not supported, try any of [%s] instead' % (expect_ladder, ', '.join(supported)))

        params = {
            'rule_path': self.rule_path,
            'plugin_path': self.plugin_path
        }

        try:
            gfwlist_file = os.path.join(self.rule_path, common.GFW_LIST_FILE)
            with open(gfwlist_file, 'r') as f:
                content = base64.decodestring(f.read())

            domains = parse_gfwlist(content.split('\n'))
            domains = reduce_domains(domains)

            params.update({
                'gfwlist_proxy_domain': domains,
            })
        except Exception, e:
            print >> sys.stderr, e.message

        try:
            user_rule_file = os.path.join(self.rule_path, 'user-rule.txt')
            with open(user_rule_file, 'r') as f:
                content = f.read()

            domains = parse_gfwlist(content.split('\n'))
            domains = reduce_domains(domains)

            params.update({
                'user_proxy_domain': domains,
            })

        except Exception, e:
            print >> sys.stderr, e.message

        return ladder_ins.gen(**params)
