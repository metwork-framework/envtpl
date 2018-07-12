# envtpl

## Status (master branch)

[![Travis](https://img.shields.io/travis/metwork-framework/envtpl.svg)](https://travis-ci.org/metwork-framework/envtpl)
[![License](https://img.shields.io/badge/license-GPL-blue.svg)](https://github.com/metwork-framework/envtpl)
[![Maturity](https://img.shields.io/badge/maturity-beta-yellow.svg)](https://github.com/metwork-framework/envtpl)
[![Maintenance](https://img.shields.io/maintenance/yes/2018.svg)](https://github.com/metwork-framework)


## What is it ?

Render jinja2 templates on the command line with shell environment variables.

This repository is a maintained fork of [andreasjansson/envtpl](https://github.com/andreasjansson/envtpl).


## How-to

Say you have a configuration file called whatever.conf that looks like this

    foo = 123
    bar = "abc"

You can use envtpl to set `foo` and `bar` from the command line by creating a file called whatever.conf.tpl

    foo = {{ FOO }}
    bar = "{{ BAR }}"

If you run

    FOO=123 BAR=abc envtpl < whatever.conf.tpl > whatever.conf

you'll get back the original whatever.conf.

You can also specify default values

    foo = {{ FOO | default(123) }}
    bar = "{{ BAR | default("abc") }}"

Running

    FOO=456 envtpl < whatever.conf.tpl > whatever.conf

will generate

    foo = 456
    bar = "abc"

This is all standard [Jinja2 syntax](http://jinja.pocoo.org/docs/templates/), so you can do things like

    {% if BAZ is defined %}
    foo = 123
    {% else %}
    foo = 456
    {% endif %}
    bar = "abc"

If an environment variable is missing, envtpl will throw an error

    $ echo '{{ FOO }} {{ BAR }}' | FOO=123 envtpl
    Error: 'BAR' is undefined

You can change this behaviour to insert empty strings instead by passing the `--allow-missing` flag.

Instead of reading from stdin and writing to stdout, you can pass the input filename as an optional positional argument,
and set the output filename with the `--output-file` (`-o`) argument.

    envtpl -o whatever.conf  whatever.conf.tpl

As a convenience, if you don't specify an output filename and the input filename ends with `.tpl`, the output filename will be the input filename without the `.tpl` extension, i.e.

    envtpl whatever.conf.tpl
    # is equivalent to
    envtpl -o whatever.conf whatever.conf.tpl

By default, envtpl will **delete** the input template file. You can keep it by passing the `--keep-template` flag.

There's a special `environment(prefix='')` function that you can use as a kind of wildcard variable. If you have `hello.tpl`

    hello = {{ FOO }}
    {% for key, value in environment('MY_') %}{{ key }} = {{ value }}
    {% endfor %}

and compile it using

    FOO=world MY_baz=qux MY_foo=bar envtpl hello.tpl

You end up with

    hello = world
    baz = qux
    foo = bar

If you need more complex data structures you can pass in JSON as a string and use the `from_json` filter to turn it into an object you can use in your template:

    FOO='[{"v": "hello"}, {"v": "world"}]' envtpl <<< '{% for x in FOO | from_json %}{{ x.v }}{% endfor %}'

gives

    helloworld

and

    FOO='{"bar": "baz"}' envtpl <<< '{{ (FOO | from_json).bar }}'

renders

    baz

Another custom filter is included: "shell". It can be used to execute commands
during template parsing. The output of the command will be injected as a result
of the filter.

For example:

    This is the system date : {{ "date"|shell }}

renders:

    This is the system date: Mon Apr 23 13:11:11 CEST 2018

Another custom filter is included: "uuid". It can be used to generate uuids
during template parsing.

For example:

    This is the uuid : {{ ""| uuid }}

renders:

    This is the uuid: ddd6103c6c0b5951b04789f8efa386f9

A last custom filter is included: "getenv". It can be used to get an environnement
variable value dynamicaly.

For example:

    {% set dynamic_environnement_variable_name = "FOO" + "BAR" %}
    This is the FOOBAR environnement variable value: {{ dynamic_environnement_variable_name|getenv }}

## API

You can also use envtpl directly from python with the function `render_string`:

```python
def render_string(string, extra_variables={},
                  die_on_missing_variable=True, extra_search_paths=[]):
    """
    Renders a templated string with envtpl.

    Args:
        string: templated string to render.
        extra_variables: dict (string: string) of variables to add to env
            for template rendering (these variables are not really added
            to environnement).
        die_on_missing_variable (boolean): if True (default), an exception
            is raised when there are some missing variables.
        extra_search_path (list): list of paths (string) for templates
            searching (inheritance, includes...).

    Returns:
        string: rendered template.
    """
```

Example:

    >>> from envtpl import render_string
    >>> x = "foo {{HOME}}"
    >>> render_string(x)
    'foo /home/bar'

## Notes

We also provide a [docker image](https://github.com/metwork-framework/docker-portable-envtpl-buildimage) to build a static/portable version with pyinstaller.

just a test
