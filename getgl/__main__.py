from os import walk, system
from pathlib import Path
from sys import argv
from typing import Iterable
import webbrowser

import download as dl


def find_funcs(func_name: str,
               paths: Iterable[str],
               with_matches: bool) -> list[Path]:
    func_name = func_name.lower()
    matches = []
    for path in paths:
        p = Path(path)
        if not (p.exists() and p.is_dir()):
            continue
        for _, _, files in walk(path):
            for f in files:
                f = p / f
                filename = f.stem.lower()
                if filename == func_name and not with_matches:
                    return [f]
                if with_matches and func_name in filename:
                    matches.append(f)
    return matches


if __name__ == '__main__':
    if len(argv) == 1:
        dl.gl()
        dl.glsl()
        exit(0)
    paths = ('gl', 'glsl')
    func_name = argv[1]
    func_paths = (find_funcs(func_name, paths, False) or
                  find_funcs(func_name, paths, True))
    if len(func_paths) == 1:
        webbrowser.open(*func_paths)
    else:
        for func_path in func_paths:
            print(func_path.absolute())
