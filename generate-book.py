#!/usr/bin/env python3

# TODO: /home/hayashi3017/git/bookshelf/book/Rust/Rustという不要な空フォルダが作成されないようにする

"""
This auto-generates the mdBook SUMMARY.md file based on the layout on the filesystem.

This generates the `src` directory based on the contents of the `text` directory.

Most RFCs should be kept to a single chapter. However, in some rare cases it
may be necessary to spread across multiple pages. In that case, place them in
a subdirectory with the same name as the RFC. For example:

    0123-my-awesome-feature.md
    0123-my-awesome-feature/extra-material.md

It is recommended that if you have static content like images that you use a similar layout:

    0123-my-awesome-feature.md
    0123-my-awesome-feature/diagram.svg

The chapters are presented in sorted-order.
"""

import os
import shutil
import subprocess
import sys

WORK_DIR = '/home/hayashi3017/git/bookshelf'

# 第一引数としてbook_titleを取得できなければ終了する
book_title = sys.argv[1] if len(sys.argv) > 1 else ""
if book_title == '':
    print("エラーが発生しました。プログラムを終了します。", file=sys.stderr)
    sys.exit(1)

# mdbookがsrc/配下をみてbuildするので、一時的に資材をsrc/配下へ配置しbuildする
# build資材はbook/配下にまとまっていく想定
def main():
    init_dir('src')
    gen_src(book_title)
    # mdbookの仕様によりsrc/SUMMARY.mdに固定されている様子、本来ならsrc/{book_title}/SUMMARY.mdとしたい
    # with open(f'src/SUMMARY.md', 'w') as summary:
        # summary.write('[Introduction](README.md)\n\n')
        # collect(summary, book_title, 0)

    # subjectsはトップのためbook/直下に配置する
    if book_title == 'subjects':
        subprocess.call(['mdbook', 'build', '-d', 'book'])
    else:
        subprocess.call(['mdbook', 'build', '-d', f'book/{book_title}'])

def init_dir(dir):
    if os.path.exists(dir):
        # Clear out src to remove stale links in case you switch branches.
        shutil.rmtree(dir)
    os.mkdir(dir)

# src/配下のファイルを生成
def gen_src(input_dir):
    # entries = [e for e in os.scandir(f'{input_dir}/src') if e.name.endswith('.md') and e.name != 'SUMMARY.md']
    entries = [e for e in os.scandir(f'{input_dir}/src') if e.name.endswith('.md')]
    print(f'entries: {entries}')
    # TODO: needs sort?
    # entries.sort(key=lambda e: e.name)
    for entry in entries:
        symlink(f'../{entry.path}', f'src/{entry.name}')

# summary(目次)に入れる文書をpath配下から再帰的に取得する
def collect(summary, path, depth):
    book_src = f'{path}/src'
    entries = [e for e in os.scandir(book_src) if e.name.endswith('.md')]
    entries.sort(key=lambda e: e.name)
    for entry in entries:
        # README.mdはトップで表示するのでsummaryからなくす
        if entry.name == 'README.md':
            continue
        indent = '    '*depth
        # .mdの削除
        name = entry.name[:-3]
        summary.write(f'{indent}- [{name}](/{path}/{name})\n')
        maybe_subdir = os.path.join(book_src, name)
        if os.path.isdir(maybe_subdir):
            collect(summary, maybe_subdir, depth+1)

def symlink(src, dst):
    if not os.path.exists(dst):
        os.symlink(src, dst)

if __name__ == '__main__':
    main()

# generate-book.pyをbook毎に呼び出したい