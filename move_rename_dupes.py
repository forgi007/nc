import argparse
from pathlib import Path

parser = argparse.ArgumentParser(
    description=
"""Move all files and directories from source_path to dest_path.
If a file exists in dest_path then the new file from source_path will be renamed (name.ext -> name_dup.ext)."
For dry run (print the commands but not run them) pass the '-dry' option."

Usage:
python3 move_rename_dupes.py [-dry] source_path dest_path""")
parser.add_argument('source_path', help='Path to move files and directories FROM.')
parser.add_argument('dest_path', help='Path to move files and directories TO.')
parser.add_argument('-a', '--action', default='dry', const='dry', nargs='?', choices=['dry', 'move'], help='dry: print the file actions but not run them. move: move files and directories (default: %(default)s)')
parser.add_argument('-d', '--dont_dup_dirs', action='store_false', help='do not duplicate existing directory names (default: duplicate existing directory names, i.e. source_path/sub1/* -> source_path/sub1_dup/.)'),
args = parser.parse_args()

src_dir=Path(args.source_path).resolve()
dst_dir=Path(args.dest_path).resolve()
action_list=[{"mkdir":dst_dir}]

def path_gen(path):
    if path[0]=='/':
        return Path('/').glob(f"{path[1:]}")
    else:
        return Path('').glob(f"{path}")

def action(f, dst_sub_dir):
    src=Path(f.resolve())
    dst=dst_sub_dir.joinpath(src.name)
    if dst.exists():
        dst=dst_sub_dir.joinpath(f"{dst.stem}_dup{dst.suffix}")

    action_list.append({"mv":(f,dst)})

_exhausted  = object()
def get_files(fn_gen, dst_sub_dir):
    while True:
        f=next(fn_gen, _exhausted)
        if f is _exhausted:
            break
        if f.is_dir():
            rel_src_dir=f.relative_to(src_dir)
            dst_sub_dir=dst_dir.joinpath(rel_src_dir)
            if dst_sub_dir.exists():
                dst_sub_dir=dst_dir.joinpath(f"{rel_src_dir}_dup")
            action_list.append({"mkdir":dst_sub_dir})
            get_files(f.iterdir(), dst_sub_dir)
        else:
            action(f, dst_sub_dir)


get_files(path_gen(f"{args.source_path}/*"), dst_dir)
for a in action_list:
    print(a)

