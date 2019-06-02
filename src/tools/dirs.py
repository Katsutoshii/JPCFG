'''
File: dirs.py
Project: src
File Created: Wednesday, 22nd May 2019 11:09:30 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Sunday, 2nd June 2019 12:15:37 am
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from typing import Iterator
from pathlib import Path

CWD = Path.cwd()
ROOTD = CWD
SRCD = ROOTD / 'src'
DATAD = ROOTD / 'data'
LARKD = DATAD / 'lark'
LARKIMGD = LARKD / 'images'
KEYAKID = DATAD / 'KeyakiTreebank-1.1'
TREEBANKD = KEYAKID / 'treebank'

def keyaki_trees(glob: str = '*') -> Iterator[Path]:
    for psdfile in TREEBANKD.glob(glob + '.psd'):
        yield psdfile
