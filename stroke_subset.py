#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 NINSTASS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Cut the stroke data of Make Me a Hanzi down to a list of characters.

Standalone on purpose: this script is published together with its output
(Arphic Public License), without any app code. The script itself is MIT.

Input:  graphics.txt from https://github.com/skishore/makemeahanzi
        (one JSON object per line: character, strokes, medians)
Output: one JSON file {"_notice": ..., "characters": {char: {strokes,
        medians}}}. Only these two keys are kept per character; the SVG
        paths and median points are copied unchanged.

Usage:
  python3 stroke_subset.py --graphics graphics.txt --chars 我你好 \\
      --out hanzi_strokes.json
"""

import argparse
import datetime
import json
import sys

NOTICE = (
    'Modified from graphics.txt of Make Me a Hanzi '
    '(https://github.com/skishore/makemeahanzi), which is derived from the '
    'fonts Arphic PL KaitiM GB and Arphic PL UKai. Changes ({date}): kept '
    'only {count} characters and only the keys "strokes" and "medians"; '
    'stroke data itself unchanged. Licensed under the Arphic Public License, '
    'see ARPHICPL.txt.'
)


def subset(graphics_path, chars):
    wanted = set(chars)
    found = {}
    with open(graphics_path, encoding='utf-8') as f:
        for line in f:
            entry = json.loads(line)
            char = entry['character']
            if char in wanted:
                found[char] = {'strokes': entry['strokes'],
                               'medians': entry['medians']}
    return found


def write(found, chars, out_path, date=None):
    date = date or datetime.date.today().isoformat()
    ordered = {c: found[c] for c in chars if c in found}
    data = {'_notice': NOTICE.format(date=date, count=len(ordered)),
            'characters': ordered}
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
        f.write('\n')
    return [c for c in chars if c not in found]


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--graphics', required=True)
    parser.add_argument('--chars', required=True,
                        help='characters to keep, as one string')
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    chars = list(dict.fromkeys(args.chars))
    missing = write(subset(args.graphics, chars), chars, args.out)
    if missing:
        print('Not in graphics.txt: ' + ''.join(missing), file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
