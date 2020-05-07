import argparse
import os
from typing import List
import requests


class PKG:
    def __init__(self, name, seen: dict, parent=None):
        self.name = name
        self.parent = parent
        self.seen = seen

    def __hash__(self):
        return self.name

    @property
    def requires(self):
        return [PKG(x, self.seen, parent=self) for x in  get_requires(self.name)]

    def add_to_seen(self):
        if self.name in self.seen:
            if not self.seen[self.name].parent and self.parent:
                self.seen[self.name] = self
            return False
        self.seen[self.name] = self
        return True

    def children(self, depth=0, maxdepth=100): # type: List[PKG]
        if depth > maxdepth:
            return
        if not self.add_to_seen():
            return
        yield depth, self
        for x in self.requires:
            yield from x.children(depth+1, maxdepth)

    def __repr__(self):
        return f'<PKG {self.name}>'


def get_json(name):
    return requests.get(f'https://pypi.org/pypi/{name}/json').json()


def get_requires(name):
    info = get_json(name)['info']
    return [x.split(' ', 1)[0].strip(';') for x in (info['requires_dist'] or []) if 'extra' not in x]


def all_pkgs_of(name: str, seen={}):
    yield from PKG(name, seen).children()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="name of pypi package")
    args = parser.parse_args()

    for depth, pkg in all_pkgs_of(args.name):
        print('    '*depth, pkg.name)

def root_pkgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path of python requirements")
    parser.add_argument("-v", "--verbose", action='store_true')
    args = parser.parse_args()

    seen = {}

    for l in open(args.path):
        l = l.strip()
        if l.startswith('#'):
            continue
        if args.verbose:
            print('==>', l)
        for depth, x in all_pkgs_of(l.split('=', 1)[0], seen):
            if args.verbose:
                print('    '* depth, x.name)

    if args.verbose:
        print('='*30)
    for x in seen.values():
        if not x.parent:
            print(x.name)

if __name__ == '__main__':
    main()
