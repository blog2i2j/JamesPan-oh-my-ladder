# coding=utf-8
from fancyladder import ladder
import json


class SSHProxy(ladder.Ladder):
    def __init__(self):
        super(SSHProxy, self).__init__()
        self._id = 'ssh-proxy'

    def id(self):
        return self._id

    @staticmethod
    def _domain_template(domain):
        return {"enabled": True, "address": domain, "subdomains": True}

    def gen(self, **kwargs):
        gfwlist_proxy_domain = kwargs['gfwlist_proxy_domain']
        user_proxy_domain = kwargs['user_proxy_domain']

        domains = []

        if gfwlist_proxy_domain:
            for domain in gfwlist_proxy_domain:
                domains.append(self._domain_template(domain))

        if user_proxy_domain:
            for domain in user_proxy_domain:
                domains.append(self._domain_template(domain))

        return {
            'whitelist.json': json.dumps({
                "whitelist": {
                    "Default": domains
                }
            }, indent=4)
        }
