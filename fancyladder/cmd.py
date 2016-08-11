# coding=utf-8
import click
import common
import os
import sys
import shutil
import urllib2
import errno
import time


@click.group()
def rule():
    pass


@rule.command('rule-cp')
@click.option('-f', '--force', is_flag=True, default=False)
@click.argument('dst', type=click.Path(exists=False))
def copy(force, dst):
    """copy default rules"""

    base_copy(common.DEFAULT_RULE_PATH, dst, force, '%s already exist, use -f flag to force overwrite' % dst)


@rule.command('gfw-update')
@click.option('-u', '--url', default=common.GFW_LIST_URL)
@click.option('-r', '--rule-path', default=common.DEFAULT_RULE_PATH)
@click.option('--timeout', default=10)
def update(url, rule_path, timeout):
    """update local gfwlist"""

    if not os.path.exists(rule_path):
        try:
            os.makedirs(rule_path)
        except OSError as exp:
            if exp.errno == errno.EEXIST and os.path.isdir(rule_path):
                pass
            else:
                raise

    try:
        response = urllib2.urlopen(url, timeout=timeout)
        body = response.read()
        response.close()

        gfwlist_file = os.path.join(rule_path, common.GFW_LIST_FILE)

        if os.path.exists(gfwlist_file):
            os.rename(gfwlist_file, os.path.join(rule_path, common.GFW_LIST_ARCHIVE % (int(time.time()))))

        with open(os.path.join(rule_path, common.GFW_LIST_FILE), 'w') as f:
            f.write(body)

    except urllib2.HTTPError, e:
        raise click.ClickException('get HTTP Status Code %s from %s' % (e.code, url))


@click.group()
def plugin():
    pass


@plugin.command('plugin-cp')
@click.option('-f', '--force', is_flag=True, default=False)
@click.argument('dst', type=click.Path(exists=False))
def copy(force, dst):
    """copy default plugins"""

    base_copy(common.DEFAULT_PLUGIN_PATH, dst, force, '%s already exist, use -f flag to force overwrite' % dst)


@click.group()
def biz():
    pass


@biz.command('gen-cfg')
@click.option('-r', '--rule-path', default=common.DEFAULT_RULE_PATH)
@click.option('-p', '--plugin-paths', default=[common.DEFAULT_PLUGIN_PATH], multiple=True)
@click.option('-o', '--output-to', default=sys.stdout)
@click.argument('ladder')
def generate(rule_path, plugin_paths, output_to, ladder):
    """generate configuration"""

    from framework import LadderFramework
    from ladder import LadderException

    rule_path = os.path.abspath(rule_path)
    plugin_paths = map(os.path.abspath, plugin_paths)

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


def main():
    click.CommandCollection(sources=[rule, plugin, biz])()


if __name__ == '__main__':
    main()
