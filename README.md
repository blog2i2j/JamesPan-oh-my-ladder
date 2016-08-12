# oh-my-ladder : Awesome Configuration Generator for Ladders

I use different network proxy App in different device to help me visit the "world wide web". I use the Surge App on iOS while SSH Proxy on macOS. My friend even use Potatso as an alternative of Surge.

These days I have tired of keeping configuration of all these Apps sync. So, that's why *oh-my-ladder* show up.

oh-my-ladder is a configuration generator with plugin architecture, especially design for ladders, both developer and user can get benefit from it.

## Install

install the latest code

```bash
sudo pip install -U git+https://github.com/JamesPan/oh-my-ladder.git
```

or a stable release

```bash
sudo pip install https://github.com/JamesPan/oh-my-ladder/archive/0.0.1.zip
```

## Usage

After installation, `ladder` command should be accessible in system path. Type `ladder` to get more information.

```
➜  ~  ladder
Usage: ladder [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  gen-cfg     generate configuration
  gfw-update  update local gfwlist
  plugin-cp   copy default plugins
  rule-cp     copy default rules
```

Use `--help` to get the usage info for each sub command.

```
➜  ~  ladder gen-cfg --help
Usage: ladder gen-cfg [OPTIONS] LADDER

  generate configuration

Options:
  -r, --rule-path TEXT     path contains proxy rules
  -p, --plugin-paths TEXT  path to find plugins
  -o, --output-to TEXT     path to save configuration, write to stdout by
                           default
  --help                   Show this message and exit.
```

Generate configuration for Surge with default template.

```
ladder gen-cfg surge
```




