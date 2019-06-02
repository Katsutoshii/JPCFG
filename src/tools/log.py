'''
File: log.py
Project: tools
File Created: Sunday, 2nd June 2019 3:52:31 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Sunday, 2nd June 2019 3:55:58 am
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from .dirs import DATAD

logfile = DATAD / 'out.txt'

def log(*args):
    print(*args)
    with open(logfile, 'a', encoding='utf8') as log:
        print(*args, file=log)
