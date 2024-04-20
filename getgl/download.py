'''
Links for downloading API and its info:

- https://registry.khronos.org/OpenGL-Refpages/gl4/html/bitfieldExtract.xhtml
- https://registry.khronos.org/OpenGL-Refpages/es2.0/xhtml/glGetShaderiv.xml
'''

from typing import Iterable
from urllib import request

from lxml import etree


def get_funcs(url: str, find_str: str, skip: Iterable[str]) -> list[str]:
    response = request.urlopen(url)
    html = bytes().join(response.readlines())
    root = etree.HTML(html)
    return [i.text for i in root.iterfind(find_str) if i.text not in skip]


if __name__ == '__main__':
    glsl_funcs = get_funcs(
        url='https://registry.khronos.org/OpenGL-Refpages/es2.0/xhtml/index.html',
        find_str='.//a[@target]',
        skip=tuple(),
    )
    gl_funcs = get_funcs(
        url='https://registry.khronos.org/OpenGL-Refpages/gl4/html/indexflat.php',
        find_str='.//a[@target]',
        skip=('Introduction', ),
    )

    print(gl_funcs)
