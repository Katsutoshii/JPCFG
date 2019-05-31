'''
File: dirs.py
Project: src
File Created: Wednesday, 22nd May 2019 11:09:30 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Friday, 31st May 2019 3:30:28 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from typing import Iterator
from pathlib import Path

CWD = Path.cwd()
ROOTD = CWD.parent
SRCD = ROOTD / 'src'
DATAD = ROOTD / 'data'
LARKD = DATAD / 'lark'
KEYAKID = DATAD / 'KeyakiTreebank-1.1'
TREEBANKD = KEYAKID / 'treebank'

def keyaki_trees(glob: str = '*') -> Iterator[Path]:
    for psdfile in TREEBANKD.glob(glob + '.psd'):
        yield psdfile
