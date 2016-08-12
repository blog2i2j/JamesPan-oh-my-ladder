# coding=utf-8
import click
import common
import os
import sys
import shutil
import urllib2
import errno
import time
import ConfigParser

pass_config = click.make_pass_decorator(ConfigParser.ConfigParser)


@click.group()
@click.pass_context
def cli(ctx):
    parser = ctx.obj
    config_file = os.environ.get('OML_CONFIG_FILE', False)
    if config_file == os.devnull:
        config_file = False
    if not config_file:
        user_dir = expenduser('~')
        if sys.platform.startswith('win') or (sys.platform == 'cli' and os.name == 'nt'):
            config_basename = 'ladder.ini'
        else:
            config_basename = 'ladder.conf'
        config_dir = os.path.join(user_dir, '.ladder')
        config_file = os.path.join(config_dir, config_basename)

    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            parser.readfp(f)


@cli.command('rule-cp')
@click.option('-f', '--force', is_flag=True, default=False, help='force copy to dst, may lost previous data')
@click.argument('dst', type=click.Path(exists=False))
def copy(force, dst):
    """copy default rules to destination path"""

    base_copy(common.DEFAULT_RULE_PATH, dst, force, '%s already exist, use -f flag to force overwrite' % dst)


@cli.command('gfw-update')
@click.option('-u', '--url', default=common.GFW_LIST_URL, help='url of gwflist.txt')
@click.option('-r', '--rule-path', default=common.DEFAULT_RULE_PATH, help='path contains proxy rules')
@click.option('--timeout', default=0, type=int, help='timeout fetching gfwlist.txt in seconds')
@pass_config
def update(config, url, rule_path, timeout):
    """update local gfwlist"""

    if config.has_section('global'):
        if config.has_option('global', 'rule-path'):
            candidate = config.get('global', 'rule-path')
            if rule_path == common.DEFAULT_RULE_PATH:
                rule_path = candidate
        if config.has_option('global', 'gfwlist-url'):
            candidate = config.get('global', 'gfwlist-url')
            if url == common.GFW_LIST_URL:
                url = candidate

    rule_path = os.path.abspath(expenduser(rule_path))

    if not os.path.exists(rule_path):
        try:
            os.makedirs(rule_path)
        except OSError as exp:
            if exp.errno == errno.EEXIST and os.path.isdir(rule_path):
                pass
            else:
                raise

    try:
        params = {}
        if timeout > 0:
            params['timeout'] = timeout
        response = urllib2.urlopen(url, **params)
        body = response.read()
        response.close()

        gfwlist_file = os.path.join(rule_path, common.GFW_LIST_FILE)

        if os.path.exists(gfwlist_file):
            os.rename(gfwlist_file, os.path.join(rule_path, common.GFW_LIST_ARCHIVE % (int(time.time()))))

        with open(os.path.join(rule_path, common.GFW_LIST_FILE), 'w') as f:
            f.write(body)

    except urllib2.HTTPError, e:
        raise click.ClickException('get HTTP Status Code %s from %s' % (e.code, url))


@cli.command('plugin-cp')
@click.option('-f', '--force', is_flag=True, default=False, help='force copy to dst, may lost previous data')
@click.argument('dst', type=click.Path(exists=False))
def copy(force, dst):
    """copy default plugins to destination path"""

    base_copy(common.DEFAULT_PLUGIN_PATH, dst, force, '%s already exist, use -f flag to force overwrite' % dst)


@cli.command('gen-cfg')
@click.option('-r', '--rule-path', default=common.DEFAULT_RULE_PATH, help='path contains proxy rules')
@click.option('-p', '--plugin-paths', default=[common.DEFAULT_PLUGIN_PATH], multiple=True, help='path to find plugins')
@click.option('-o', '--output-to', default=sys.stdout, help='path to save configuration, write to stdout by default')
@click.argument('ladder')
@pass_config
def generate(config, rule_path, plugin_paths, output_to, ladder):
    """generate configuration"""

    if config.has_section('global'):
        if config.has_option('global', 'rule-path'):
            candidate = config.get('global', 'rule-path')
            if rule_path == common.DEFAULT_RULE_PATH:
                rule_path = candidate
        if config.has_option('global', 'plugin-paths'):
            candidate = config.get('global', 'plugin-paths')
            candidate = map(str.strip, candidate.split(','))
            if plugin_paths == (common.DEFAULT_PLUGIN_PATH,):
                plugin_paths = candidate

    from framework import LadderFramework
    from ladder import LadderException

    rule_path = os.path.abspath(expenduser(rule_path))
    plugin_paths = map(lambda p: os.path.abspath(expenduser(p)), plugin_paths)

    framework = LadderFramework(rule_path, plugin_paths)
    try:
        out = framework.run(ladder)
    except LadderException, e:
        raise click.ClickException(e.message)

    if out:
        for filename, content in out.iteritems():
            if output_to == sys.stdout:
                output_to.write('\n'.join([filename, '---', '']))
                output_to.write(content)
                output_to.write('\n')
            else:
                with open(os.path.join(output_to, filename), 'w') as f:
                    f.write(content + '\n')


def base_copy(src, dst, force, on_fail_msg):
    if os.path.exists(dst):
        if force:
            shutil.rmtree(dst, ignore_errors=True)
        else:
            raise click.ClickException(on_fail_msg)

    shutil.copytree(src, dst)


def expenduser(path):
    expended = os.path.expanduser(path)
    if path.startswith('~/') and expended.startswith('//'):
        expended = expended[1:]
    return expended


def main():
    click.CommandCollection(sources=[cli(obj=ConfigParser.ConfigParser())])()


if __name__ == '__main__':
    main()
