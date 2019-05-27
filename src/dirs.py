'''
File: dirs.py
Project: src
File Created: Wednesday, 22nd May 2019 11:09:30 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Sunday, 26th May 2019 10:10:47 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

from pathlib import Path

CWD = Path.cwd()
ROOTD = CWD.parent
SRCD = ROOTD / 'src'
DATAD = ROOTD / 'data'
KEYAKID = DATAD / 'KeyakiTreebank-1.1'
TREEBANKD = KEYAKID / 'treebank'
