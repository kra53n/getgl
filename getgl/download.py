from pathlib import Path
from typing import Iterable
from urllib import request
from urllib.error import HTTPError

from lxml import etree


_GLSL_BASE_URL = 'https://registry.khronos.org/OpenGL-Refpages/es2.0/xhtml/'
_GL_BASE_URL = 'https://registry.khronos.org/OpenGL-Refpages/gl4/html/'


def _get_url(base: str, what: str, file_extension: str):
    return f'{base}{what}.{file_extension}'


def _get_funcs(url: str, find_str: str, skip: Iterable[str]) -> list[str]:
    with request.urlopen(url) as response:
        html = bytes().join(response.readlines())
    root = etree.HTML(html)
    return [i.text for i in root.iterfind(find_str) if i.text not in skip]


def _download_func(base_url: str,
                   dir_name: str,
                   func_name: Iterable[str],
                   file_extension: str):
    p = Path(dir_name) / f'{func_name}.{file_extension}'
    if p.exists():
        return
    func_url = _get_url(base_url, func_name, file_extension)
    with request.urlopen(func_url) as response:
        html = bytes().join(response.readlines())
    p.write_bytes(html)


def _download_funcs(base_url: str,
                    dir_name: str,
                    func_names: Iterable[str],
                    file_extension: str):
    p = Path(dir_name)
    if not (p.exists() and p.is_dir()):
        p.mkdir()
    for func_name in func_names:
        try:
            _download_func(base_url,
                           dir_name,
                           func_name,
                           file_extension)
        except HTTPError as e:
            # if 404 NotFound error occured that means function already
            # in another file
            if e.code == 404:
                continue
            raise e


def glsl():
    funcs = _get_funcs(url=_get_url(_GLSL_BASE_URL, 'index', 'html'),
                       find_str='.//a[@target]',
                       skip=tuple())
    _download_funcs(_GLSL_BASE_URL, 'glsl', funcs, 'xml')


def gl():
    funcs = _get_funcs(url=_get_url(_GL_BASE_URL, 'indexflat', 'php'),
                       find_str='.//a[@target]',
                       skip=('Introduction', ))
    _download_funcs(_GL_BASE_URL, 'gl', funcs, 'xhtml')
    
        


if __name__ == '__main__':
    glsl_funcs = _get_funcs(url=_get_url(_GLSL_BASE_URL, 'index', 'html'),
                            find_str='.//a[@target]',
                            skip=tuple())
    gl_funcs = _get_funcs(url=_get_url(_GL_BASE_URL, 'indexflat', 'php'),
                          find_str='.//a[@target]',
                          skip=('Introduction', ))
    _download_funcs(_GLSL_BASE_URL, 'glsl', glsl_funcs, 'xml')
    _download_funcs(_GL_BASE_URL, 'gl', gl_funcs, 'xhtml')
