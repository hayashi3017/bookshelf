#!/usr/bin/env python3

"""
Deprecated.
Use build.py instead of this, because this is not good at native mdbook build support.
ex) meta data (book title) rendering, mermaid-support with mdbook-mermaid

`mdbook build`のラッパーであり、mdbookを階層的にビルドします
第一引数にmdbookのパス名 (タイトルも同じ想定)を指定してください、例外として`home`を指定した場合は/book直下にビルド成果物を配置します
  例) `mdbook init home --title home --ignore git`などによって/homeをルートとするmdbookが存在する場合、`python3 generate-book.py home`で/book/配下にビルド成果物を配置する
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

    # homeはトップのためbook/直下に配置する
    if book_title == 'home':
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

# get file recursively
def get_files(directory, extention):
    entries = []
    for entry in os.scandir(directory):
        if entry.is_file() and entry.name.endswith(extention):
            entries.append(entry)
        elif entry.is_dir():
            entries.extend(get_files(entry.path, extention))
    return entries

# get dirctory recursively
def get_dir(directory):
    entries = []
    for entry in os.scandir(directory):
        if entry.is_dir():
            entries.append(entry)
            entries.extend(get_dir(entry.path))
    return entries

# src/配下のファイルを生成
def gen_src(input_dir):
    # 先にdirectoryを再帰的に初期化する
    dirs = get_dir(input_dir)
    for dir in dirs:
        new_dir = dir.path[len(f'{input_dir}/'):]
        init_dir(new_dir)
    # src/配下のMarkdownファイル
    entries = get_files(f'{input_dir}/src', '.md')
    for entry in entries:
        # input_dirからsrc/配下への付け替え
        # 例）rust/src/standard/index.mdからstandard/index.mdへ
        relative_path = entry.path[len(f'{input_dir}/src/'):]
        dir_count = relative_path.count('/')
        pre_path = '../' * dir_count
        symlink(f'../{pre_path}{entry.path}', f'src/{relative_path}')
    # src/images/配下の画像ファイル
    if os.path.exists(f'{input_dir}/src/images'):
      entries = get_files(f'{input_dir}/src/images', ('.png', '.svg'))
      if len(entries) > 0:
        for entry in entries:
            symlink(f'../../{entry.path}', f'src/images/{entry.name}')

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
