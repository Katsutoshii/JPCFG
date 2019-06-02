'''
File: main.py
Project: src
File Created: Wednesday, 22nd May 2019 11:04:39 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Sunday, 2nd June 2019 1:42:13 am
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from sys import argv, path
from test import segment_test, parse_test, full_test
if __name__ == "__main__":
    path.append('.')
    tests = {
        'pcfg': parse_test,
        'seg': segment_test,
        'full': full_test
    }
    try:
        mode = argv[1]
        if mode not in tests:
            raise Exception
    except Exception as e:
        print("Usage: python src/main.py <pcfg|seg|full>")

    tests[mode]()
