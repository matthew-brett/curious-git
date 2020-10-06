#!/usr/bin/env python
""" A little utility to display the structure of directory trees

Inspired by:

http://lorenzod8n.wordpress.com/2007/12/13/creating-a-tree-utility-in-python-part-2/

with thanks.

This version is my own copyright (Matthew Brett) released under 2-clause BSD
"""
from __future__ import print_function, division

import sys
from os import getcwd, listdir, stat
from os.path import basename, join as pjoin, isfile, isdir, sep as dir_sep
import re
from argparse import ArgumentParser
from locale import getpreferredencoding

try:
    string_type = basestring
except NameError:
    string_type = str

# Unicode constants for constructing the tree trunk and branches
ALONG = u'\u2500'
DOWN = u'\u2502'
DOWN_RIGHT = u'\u251c'
ELBOW_RIGHT = u'\u2514'
BLUE = u'\033[94m'
ENDC = u'\033[0m'
DOWN_RIGHT_ALONG = DOWN_RIGHT + ALONG * 2 + u" "
ELBOW_RIGHT_ALONG = ELBOW_RIGHT + ALONG * 2 + u" "
CONTINUE_INDENT = DOWN + u' ' * 3
FINISH_INDENT = u' ' * 4

# File sizes
KB = 1024
MB = KB * KB
GB = MB * KB


def human_size(path):
    try:
        size = stat(path).st_size
    except OSError:
        return u"<cannot read file>"
    for divisor, suffix in ((GB, u'G'),
                            (MB, u'M'),
                            (KB, u'K')):
        divided = size / divisor
        if divided < 1:
            continue
        if round(divided) < 10:
            return u'{:.1f}{}'.format(divided, suffix)
        return u'{:.0f}{}'.format(round(divided), suffix)
    return u'{:d}B'.format(size)


class TreeMaker(object):

    def __init__(self,
                 dir_sort_func=None,
                 elide_dirs=None,
                 unelide_dirs=None,
                 label_func=None,
                 colors=False,
                 show_size=False):
        """ Initialize object for showing trees as strings

        dir_sort_func : None or callable, optional
            If None, sort directory entries by name.  If callable, call with
            single argument ``path`` to return directory entries in desired
            order.  Paths returned are full paths.
        elide_dirs : None or str or regexp or sequence or callable, optional
            str containing regexp or regexp or sequence of (str or regexp) or
            callable identifying directories for which to elide contents.
            Elide if (any) regexp matches or callable returns True.  Callable
            accepts single argument ``path``.
        unelide_dirs : None or str or regexp or sequence or callable, optional
            str containing regexp or regexp or sequence of (str or regexp) or
            callable identifying directories for which to skip elide check.
            Skip if (any) regexp matches or callable returns True.  Callable
            accepts single argument ``path``.
        label_func : None or callable, optional
            Function accepting path name and returning string to display.
            Defaults to display of basename, modified as per `colors` and
            `show_size` arguments to this constructor.
        colors : {False, True}
            Whether to add colors to output.  Ignored if `label_func` is not
            None.
        show_size : {False, True}, optional
            If True, show size next to file name in human readable format.
            Ignored if `label_func` is not None.
        """
        self.show_size = show_size
        self.dir_sort_func = (dir_sort_func if dir_sort_func is not None
                              else self._default_sort_func)
        self.elider = self._make_check_func(elide_dirs)
        self.unelider = self._make_check_func(unelide_dirs)
        self.label_func = (self._default_label_func if label_func is None
                           else label_func)
        self.colors = bool(colors)

    def _default_label_func(self, path):
        base = basename(path)
        is_dir = isdir(path)
        path_str = self.color_path(base) if is_dir else base
        if self.show_size and not is_dir:
            path_str += u' [{}]'.format(human_size(path))
        return path_str

    def _default_sort_func(self, path):
        return [pjoin(path, f) for f in sorted(listdir(path))]

    def _make_check_func(self, check_strs):
        if hasattr(check_strs, '__call__'):
            return check_strs
        if check_strs is None or len(check_strs) == 0:
            return lambda p : False
        if isinstance(check_strs, string_type):
            check_strs = [check_strs]
        check_res = [re.compile(check_re) for check_re in check_strs]

        def checker(path):
            for check_re in check_res:
                if check_re.search(path):
                    return True
            return False

        return checker

    def as_string(self, root_path=None):
        """ Return string with tree structure starting from `root_path`

        Parameters
        ----------
        root_path : None or str, optional
            path from which to print directory tree structure.  If None, use
            current directory.
        indent_str : str, optional
            prefix to print for every entry in the tree.  Usually '', and then
            set by recursion into the function when printing subdirectories.

        Returns
        -------
        tree_str : str
            String representing tree
        """
        if root_path is None:
            root_path = getcwd()
        return self._tree_string(root_path, indent_str=u'')

    def _tree_string(self, root_path, indent_str):
        # Full paths returned
        paths = self.dir_sort_func(root_path)
        if len(paths) == 0:
            return
        lines = []
        for path in paths:
            lines.append(self._path_lines(path,
                                          indent_str,
                                          path == paths[-1]))
        return '\n'.join(lines)

    def color_path(self, path):
        if self.colors:
            return BLUE + path + ENDC
        return path

    def elision_str(self, path):
        n_files = n_dirs = 0
        out_parts = []
        for fname in listdir(path):
            full_path = pjoin(path, fname)
            if isfile(full_path):
                n_files += 1
            elif isdir(full_path):
                n_dirs += 1
        if n_files:
            out_parts.append(u'{} {}'.format(
                n_files, 'files' if n_files > 1 else 'file'))
        if n_dirs:
            out_parts.append(u'{} {}'.format(
                n_dirs, 'directories' if n_dirs > 1 else 'directory'))
        if len(out_parts) == 0:
            out_parts = ['empty']
        return u'(%s)' % u'; '.join(out_parts)

    def _path_lines(self, path, indent_str, last_entry=False):
        """ Return str for single `path`

        Parameters
        ----------
        path : str
            file name or directory name
        indent_str : str
            string to prefix to entry for this `path`
        last_entry : bool, optional
            Whether this is the last entry in a list of paths.

        Returns
        -------
        path_lines : str
            String representing this path.  If `path` is a directory will have one
            line per entry in the directory.
        """
        have_dir = isdir(path)
        leader = ELBOW_RIGHT_ALONG if last_entry else DOWN_RIGHT_ALONG
        path_str = indent_str + leader + self.label_func(path)
        if not have_dir:
            return path_str
        extra_indent = FINISH_INDENT if last_entry else CONTINUE_INDENT
        indent_str += extra_indent
        if not self.unelider(path) and self.elider(path):
            return u'{}\n{}{}'.format(path_str,
                                      indent_str,
                                      self.elision_str(path))
        subdir_lines = self._tree_string(path, indent_str)
        if subdir_lines:
            path_str = path_str + '\n' + subdir_lines
        return path_str


def get_parser():
    parser = ArgumentParser()
    parser.add_argument('--hasta', type=str,
                        help='regex matching line before which to '
                        'truncate output')
    parser.add_argument('--colors', action='store_true')
    parser.add_argument('--no-show-size', action='store_true')
    parser.add_argument('--elide-dir', action='append',
                       help='regex(es) for directories to elide')
    parser.add_argument('--unelide-dir', action='append',
                       help='regex(es) for directories to not elide')
    parser.add_argument('--encoding', default=getpreferredencoding(),
                       help='output encoding')
    return parser


def printout(s):
    return sys.stdout.write(s + '\n')


def output_tree(args, klass=TreeMaker):
    # Basename needs slash removed
    root_dir = args.root_dir
    if root_dir.endswith(dir_sep):
        root_dir = args.root_dir[:-1]
    hasta = re.compile(args.hasta) if args.hasta else None
    tree_maker = klass(show_size=not args.no_show_size,
                       elide_dirs=args.elide_dir,
                       unelide_dirs=args.unelide_dir,
                       colors=args.colors)
    printout(tree_maker.color_path(basename(root_dir)))
    tree_str = tree_maker.as_string(root_dir)
    if tree_str is None:
        return
    for line in tree_str.splitlines():
        if hasta and hasta.search(line):
            printout('...')
            break
        printout(line)


def main():
    parser = get_parser()
    parser.add_argument('root_dir',
                        help='directory for which to show tree repr')
    output_tree(parser.parse_args())


if __name__ == '__main__':
    main()
