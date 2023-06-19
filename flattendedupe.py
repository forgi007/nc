from pathlib import Path
import argparse
from edit_tui import edit_tui
from read_jdupes import read_jdupes

# get keys and mouse click: https://pypi.org/project/pynput/

parser = argparse.ArgumentParser(
    description=
"""Move all files and directories from source_path to dest_path.
If a file exists in dest_path then the new file from source_path will be renamed (name.ext -> name_dup.ext)."
For dry run (print the commands but not run them) pass the '-dry' option."

Usage:
python3 flattendedupe.py [-dry] source_path dest_path""")
parser.add_argument('-d','--jdupes', help='json file containing duplicates, generated with "jdupes -jzrS source_path dest_path".')
parser.add_argument('source_path', nargs='+', help='Path to move files and directories FROM, or backup data source path. One or more path can be provided.')
parser.add_argument('dest_path', nargs='?', default=None, help='Path to move files and directories TO, or consolidated backup destination path. Zero or one path can be provided.')
parser.add_argument('-a', '--action', default='dry', const='dry', nargs='?', choices=['dry', 'move'], help='dry: print the file actions but not run them. move: move files and directories (default: %(default)s)')
parser.add_argument('-n', '--dont_dup_dirs', action='store_false', help='do not duplicate existing directory names (default: duplicate existing directory names, i.e. source_path/sub1/* -> dest_path/sub1_dup/.)'),
args = parser.parse_args()

file_actions=[]

def path_gen(path):
    if path[0]=='/':
        return Path('/').glob(f"{path[1:]}")
    else:
        return Path('').glob(f"{path}")

def add_action(f, dst_sub_dir, action_list):
    src=Path(f.resolve())
    dup=0
    if dst_sub_dir is not None:
        dst=dst_sub_dir.joinpath(src.name)
        while dst.exists():
            dst=dst_sub_dir.joinpath(f"{dst.stem}_dup{dup}{dst.suffix}" if dup else f"{dst.stem}_dup{dst.suffix}")
            dup+=1
    else:
        dst=None
    action_list.append({"action":"mv", "src":f, "dst":dst, "file_dupe_name":dup})

def build_file_actions(file_actions:list):
    _exhausted  = object()
    def get_files(fn_gen, dst_sub_dir, action_list):
        while True:
            f=next(fn_gen, _exhausted)
            if f is _exhausted:
                break
            if f.is_dir():
                # only files
                n_files = len([p for p in f.iterdir() if p.is_file()])
                # only directories
                n_dirs = len([p for p in f.iterdir() if p.is_dir()])                

                dup=0
                if dst_sub_dir is not None:
                    rel_src_dir=f.relative_to(src_dir)
                    dst_sub_dir=dst_dir.joinpath(rel_src_dir)
                    while dst_sub_dir.exists():
                        dst_sub_dir=Path(str(dst_sub_dir)+(f"_dup{dup}" if dup else "_dup"))
                        dup+=1
                child_action_list=[]
                action_list.append({"action":"mvdir", "src":f, "dst":dst_sub_dir, "dir_dupe_name":dup, "child":child_action_list})
                get_files(f.iterdir(), dst_sub_dir, child_action_list)
            else:
                add_action(f, dst_sub_dir, action_list)

    dst_dir=Path(args.dest_path).resolve() if args.dest_path is not None else None
    for src in args.source_path:
        src_dir=Path(src).resolve() 
        if dst_dir is not None and dst_dir.is_relative_to(src_dir):
            print(f"dest_path {dst_dir} should be outside of source_path {src_dir} or None.")
            exit(0)
        file_actions.append({"action":"mvdir","src":src_dir,"dst":dst_dir, "child":[]})
        get_files(path_gen(f"{str(src_dir)}/*"), dst_dir, file_actions[-1]["child"])

def fa_add_jdupe_info(file_actions, jdupes):
    pass

build_file_actions(file_actions)
jdupes=read_jdupes(args.jdupes)
fa_add_jdupe_info(file_actions, jdupes)
edit_tui(file_actions)