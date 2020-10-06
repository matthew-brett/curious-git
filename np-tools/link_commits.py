#!/usr/bin/env python
""" Link commits with hashes of the messages
"""

import sys
from os.path import (dirname, join as pjoin, abspath)

from hashlib import sha1


MY_PATH = dirname(__file__)
sys.path.append(abspath(MY_PATH))
from nobel_prize import (DEFAULT_PATH, COMMIT_MSG_FNAME)

LINKS = (('2', ('1',)),
         ('3', ('2',)),
         ('4', ('3',)),
         ('5', ('4',)),
         ('6', ('5',)),
         ('7', ('6',)),
         ('7_josephine', ('6',)),
         ('8', ('7', '7_josephine')),
        )


def msg_for(suffix):
    return pjoin(DEFAULT_PATH, 'snapshot_' + suffix, COMMIT_MSG_FNAME)


def read_file(fname):
    with open(fname, 'rt') as fobj:
        contents = fobj.read()
    return contents


def sha1_for(fname):
    text = read_file(fname).encode('latin1')
    return sha1(text).hexdigest()



def make_links(link_from, link_tos):
    shas = [sha1_for(msg_for(lt)) for lt in link_tos]
    parents = 'Parents: {}\n'.format(' '.join(shas))
    from_fname = msg_for(link_from)
    from_msg = read_file(from_fname)
    with open(from_fname, 'wt') as fobj:
        fobj.write(from_msg)
        fobj.write(parents)


def main():
    for link_from, link_tos in LINKS:
        make_links(link_from, link_tos)


if __name__ == '__main__':
    main()
