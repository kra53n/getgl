'''
Links for downloading API and its info:

- https://registry.khronos.org/OpenGL-Refpages/gl4/html/bitfieldExtract.xhtml
- https://registry.khronos.org/OpenGL-Refpages/es2.0/xhtml/glGetShaderiv.xml
'''

from typing import Iterable
from urllib import request

from lxml import etree


GLSL_BASE_URL = 'https://registry.khronos.org/OpenGL-Refpages/es2.0/xhtml/'
GL_BASE_URL = 'https://registry.khronos.org/OpenGL-Refpages/gl4/html/'


def get_url(base: str, what: str, ext: str):
    return f'{base}{what}.{ext}'


def get_funcs(url: str, find_str: str, skip: Iterable[str]) -> list[str]:
    response = request.urlopen(url)
    html = bytes().join(response.readlines())
    root = etree.HTML(html)
    return [i.text for i in root.iterfind(find_str) if i.text not in skip]


def download(what: str):
    match what:
        case 'glsl':
            pass
        case 'gl':
            pass
    raise Exception("`what` waiting 'glsl' or 'gl' string")


if __name__ == '__main__':
    from pprint import pprint
    glsl_funcs = get_funcs(
        url=get_url(GLSL_BASE_URL, 'index', 'html'),
        find_str='.//a[@target]',
        skip=tuple(),
    )
    gl_funcs = get_funcs(
        url=get_url(GL_BASE_URL, 'indexflat', 'php'),
        find_str='.//a[@target]',
        skip=('Introduction', ),
    )

    pprint(glsl_funcs)
    pprint(gl_funcs)
    # download('glsl')
