#!/usr/bin/env python3

"""
`mdbook build`のラッパーであり、mdbookを階層的にビルドします
第一引数にmdbookのパス名 (タイトルも同じ想定)を指定してください、例外として`subjects`を指定した場合は/book直下にビルド成果物を配置します
  例) `mdbook init subjects --title subjects --ignore git`などによって/subjectsをルートとするmdbookが存在する場合、`python3 generate-book.py subjects`で/book/配下にビルド成果物を配置する
  例) `mdbook init foo --title foo --ignore git`などによって/fooをルートとするmdbookが存在する場合、`python3 generate-book.py foo`で/book/foo/配下にビルド成果物を配置する

"""

import os
import shutil
import subprocess
import sys

# mdbookがsrc/配下をみてbuildするので、一時的に資材をsrc/配下へ配置しbuildする
# build資材はbook/配下にまとまっていく想定
def main(book_title):
    init_dir('src')
    gen_src(book_title)

    # subjectsはトップのためbook/直下に配置する
    if book_title == 'subjects':
        result = subprocess.call(['mdbook', 'build', '-d', 'book'])
    else:
        result = subprocess.call(['mdbook', 'build', '-d', f'book/{book_title}'])
    # TODO: test
    if result != 0:
        print("Error: An error occurred during the execution of mdbook build.", file=sys.stderr)
        sys.exit(1)

def init_dir(dir):
    if os.path.exists(dir):
        # Clear out src to remove stale links in case you switch branches.
        shutil.rmtree(dir)
    os.mkdir(dir)

# src/配下のファイルを生成
def gen_src(input_dir):
    entries = [e for e in os.scandir(f'{input_dir}/src') if e.name.endswith('.md')]
    for entry in entries:
        symlink(f'../{entry.path}', f'src/{entry.name}')

def symlink(src, dst):
    if not os.path.exists(dst):
        os.symlink(src, dst)

if __name__ == '__main__':
    # 第一引数としてbook_titleを取得できなければ終了する
    book_title = sys.argv[1] if len(sys.argv) > 1 else ""
    if book_title == '':
        print("Error: No argument provided. Please specify the book title.", file=sys.stderr)
        sys.exit(1)
    # FIXME: book_titleの検証、dirになければ適切なエラーを返す
    main(book_title)
