from pathlib import Path
import argparse
from edit_tui import edit_tui

# get keys and mouse click: https://pypi.org/project/pynput/

parser = argparse.ArgumentParser(
    description=
"""Move all files and directories from source_path to dest_path.
If a file exists in dest_path then the new file from source_path will be renamed (name.ext -> name_dup.ext)."
For dry run (print the commands but not run them) pass the '-dry' option."

Usage:
python3 backup_merge.py [-dry] source_path dest_path""")
parser.add_argument('source_path', help='Path to move files and directories FROM.')
parser.add_argument('dest_path', help='Path to move files and directories TO.')
parser.add_argument('-a', '--action', default='dry', const='dry', nargs='?', choices=['dry', 'move'], help='dry: print the file actions but not run them. move: move files and directories (default: %(default)s)')
parser.add_argument('-d', '--dont_dup_dirs', action='store_false', help='do not duplicate existing directory names (default: duplicate existing directory names, i.e. source_path/sub1/* -> dest_path/sub1_dup/.)'),
args = parser.parse_args()

src_dir=Path(args.source_path).resolve()
dst_dir=Path(args.dest_path).resolve()
# TODO: dst_dir should be outside of src_dir
file_actions={"action":"mvdir","src":src_dir,"dst":dst_dir, "child":[]}

def path_gen(path):
    if path[0]=='/':
        return Path('/').glob(f"{path[1:]}")
    else:
        return Path('').glob(f"{path}")

def add_action(f, dst_sub_dir, action_list):
    src=Path(f.resolve())
    dst=dst_sub_dir.joinpath(src.name)
    dup=0
    while dst.exists():
        dst=dst_sub_dir.joinpath(f"{dst.stem}_dup{dup}{dst.suffix}" if dup else f"{dst.stem}_dup{dst.suffix}")
        dup+=1

    action_list.append({"action":"mv", "src":f, "dst":dst, "file_dupe_name":dup})

def build_file_actions():
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

                rel_src_dir=f.relative_to(src_dir)
                dst_sub_dir=dst_dir.joinpath(rel_src_dir)
                dup=0
                while dst_sub_dir.exists():
                    dst_sub_dir=Path(str(dst_sub_dir)+(f"_dup{dup}" if dup else "_dup"))
                    dup+=1
                child_action_list=[]
                action_list.append({"action":"mvdir", "src":f, "dst":dst_sub_dir, "dir_dupe_name":dup, "child":child_action_list})
                get_files(f.iterdir(), dst_sub_dir, child_action_list)
            else:
                add_action(f, dst_sub_dir, action_list)

    get_files(path_gen(f"{args.source_path}/*"), dst_dir, file_actions["child"])

build_file_actions()
edit_tui(file_actions)