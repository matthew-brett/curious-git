#!/usr/bin/env python
""" Utility to make dot graph from snapshot directories

"""

import sys
from os.path import abspath, dirname, join as pjoin
from glob import glob
from argparse import ArgumentParser
from hashlib import sha1

MY_PATH = dirname(__file__)
sys.path.append(abspath(MY_PATH))
from nobel_prize import (DEFAULT_PATH, COMMIT_MSG_FNAME, read_info)


class Node(object):

    default_attrs = dict(
        shape='box',
        style='rounded,filled',
        color='skyblue4',
        fillcolor='slategray1')

    _known_nodes = {}

    def __init__(self, name,
                 label=None,
                 link_to=(),
                 **attrs):
        self.name = name
        label = name if label is None else label
        self.link_to = []
        for node in link_to:
            self.add_link(node)
        filled = self.default_attrs.copy()
        filled.update(attrs)
        filled['label'] = label
        self.attrs = filled
        self._known_nodes[self] = name

    def add_link(self, node):
        # Allow lookup by node
        if node in self._known_nodes:
            node = self.known_nodes[node]
        self.link_to.append(node)

    def __str__(self):
        attr_str = ', '.join('{}="{}"'.format(key, value)
                             for key, value in self.attrs.items())
        link_lines = '\n'.join('"{}" -> "{}"'.format(self.name, to_name)
                               for to_name in self.link_to)
        return '"{name}" [{attr_str}]\n{link_lines}'.format(
            name=self.name, attr_str=attr_str, link_lines=link_lines)


class JNode(Node):
    default_attrs = Node.default_attrs.copy()
    default_attrs['color'] = 'indianred4'
    default_attrs['fillcolor'] = 'lightpink'


class Graph(object):
    def __init__(self, name, nodes):
        self.name = name
        self.nodes = nodes

    def __str__(self):
        node_lines = '\n'.join(str(n) for n in self.nodes)
        return 'digraph "{name}" {{\n{node_lines}}}'.format(
            name=self.name,
            node_lines=node_lines)


AUTHOR2NODE_CLASS = {
    'I. M. Awesome': Node,
    'J. S. Rightway': JNode}


def get_parser():
    parser = ArgumentParser()
    parser.add_argument('root_dir',
                        default=DEFAULT_PATH,
                        nargs='?',
                        help='directory from which to get graph info')
    return parser


def main():
    """ Show graph for snapshots """
    args = get_parser().parse_args()
    root_dir = args.root_dir
    globber = pjoin(root_dir, '*', COMMIT_MSG_FNAME)
    nodes = []
    for message_fname in glob(globber):
        info = read_info(message_fname)
        sha = sha1(info['message'].encode('latin1')).hexdigest()
        node_class = AUTHOR2NODE_CLASS[info['author']]
        node = node_class(name=sha,
                          label='\n'.join((sha, info['notes'])),
                          link_to=info['parents'])
        nodes.append(node)
    print(Graph('nobel_prize', nodes))


if __name__ == '__main__':
    main()
