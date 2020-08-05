from __future__ import print_function
import argparse
import os
import errno
import sys
import envtpl
import shutil
from binaryornot.check import is_binary


def mkdir_p(path):
    """Make a directory recursively (clone of mkdir -p).

    Thanks to http://stackoverflow.com/questions/600268/
        mkdir-p-functionality-in-python .

    Any exceptions are catched internally.
    If the directory already exists, True is returned.

    Args:
        path (string): complete path to create.

    Returns:
        boolean: True if the directory exists at the end.

    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            return True
        else:
            return False
    return True


def check_directory_or_create_it_or_die(directory):
    res = mkdir_p(directory)
    if not res:
        print("ERROR: can't create %s as a directory" %
              directory, file=sys.stderr)
        sys.exit(1)


def main():
    argparser = argparse.ArgumentParser(description="apply envtpl recursively")
    argparser.add_argument(
        "SOURCE_DIRECTORY",
        help="full path of the source directory"
    )
    argparser.add_argument(
        "TARGET_DIRECTORY",
        help="full path of the target directory "
        "(will be created if it doesn't exist)"
    )
    argparser.add_argument(
        "--die-on-missing",
        action="store_true",
        help="if set, die on missing variables"
    )
    argparser.add_argument(
        "--extra-var",
        default=[],
        action="append",
        help="extra variable to set (use coma to separate key and value) "
        "(can be used several times)"
    )
    argparser.add_argument(
        "--extra-search-path",
        default=[],
        action="append",
        help="path for templates searching (inheritance, includes...) "
        "(can be used several times)"
    )
    args = argparser.parse_args()
    source_directory = os.path.abspath(args.SOURCE_DIRECTORY)
    target_directory = os.path.abspath(args.TARGET_DIRECTORY)
    if not os.path.isdir(source_directory):
        print("ERROR: %s is not a directory" %
              source_directory, file=sys.stderr)
        sys.exit(1)
    check_directory_or_create_it_or_die(target_directory)
    for root, dirs, files in os.walk(source_directory):
        if root == source_directory:
            target_root = target_directory
        else:
            target_root = os.path.join(target_directory,
                                       root[(len(source_directory) + 1):])
        for d in dirs:
            tmp = os.path.join(target_root, d)
            res = mkdir_p(tmp)
            if not res:
                raise Exception("can't create %s directory" % tmp)
        for f in files:
            source = os.path.join(root, f)
            target = os.path.join(target_root, f)
            if is_binary(source):
                shutil.copy(source, target)
            else:
                with open(source, "r") as f:
                    c = f.read()
                with open(target, "w") as f:
                    newc = envtpl.render_string(
                        c,
                        extra_variables={x.split(',')[0]: x.split(',')[1]
                                         for x in args.extra_var},
                        die_on_missing_variable=args.die_on_missing,
                        extra_search_paths=args.extra_search_path
                    )
                    f.write(newc)
