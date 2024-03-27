#!/usr/bin/env python3

"""
`mdbook build`のラッパーであり、mdbookを階層的にビルドします

"""

import os
import shutil
import subprocess
import sys

# build資材はbook/配下にまとまっていく想定
def main(book_title):
    os.chdir(book_title)
    # homeはトップのためbook/直下に配置する
    if book_title == 'home':
        result = subprocess.call(['mdbook', 'build', '-d', '../book'])
    else:
        result = subprocess.call(['mdbook', 'build', '-d', f'../book/{book_title}'])
    # TODO: test
    if result != 0:
        print("Error: An error occurred during the execution of mdbook build.", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    # 第一引数としてbook_titleを取得できなければ終了する
    book_title = sys.argv[1] if len(sys.argv) > 1 else ""
    if book_title == '':
        print("Error: No argument provided. Please specify the book title.", file=sys.stderr)
        sys.exit(1)
    # FIXME: book_titleの検証、dirになければ適切なエラーを返す
    main(book_title)
