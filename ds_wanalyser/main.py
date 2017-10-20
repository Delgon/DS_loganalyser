#!/usr/bin/env python
# encoding: utf-8

import sys
from ds_wanalyser.ds_parser.ds_parser import Parser


source_file = r"E:\bmolle\Documents\workspace\learnpy\WoWCombatLog-split-2017-10-15T15-09-32.594Z.txt"


def main():
    parser = Parser(source_file)
    parser.parse()


if __name__ == '__main__':
    sys.exit(main())