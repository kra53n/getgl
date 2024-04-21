from os import walk, system
from pathlib import Path
import webbrowser
from sys import argv

import download as dl


if len(argv) == 1:
    dl.gl()
    dl.glsl()
    exit(0)

func_name = argv[1].lower()
paths = ('gl', 'glsl')
for path in paths:
    p = Path(path)
    if not (p.exists() and p.is_dir()):
        continue
    go_out = False
    for _, _, files in walk(path):
        for f in files:
            f = p / f
            filename = f.stem.lower()
            if filename == func_name:
                f = str(f.absolute())
                webbrowser.open(f)
                go_out = True
                break
        if go_out:
            break
    if go_out:
        break
