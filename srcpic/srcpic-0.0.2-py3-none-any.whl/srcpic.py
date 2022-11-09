import numpy as np
from PIL import Image
from docopt import docopt

_name = 'srcpic'
_version = '0.0.2'
_cli = f"""{_name} Create a source code picture.

Usage:
  {_name} [options] <input> <output>

Options:
  -h --help     Show this screen.
  -v --version  Show version.
  -r --reverse  Reverse to create src from a picture.
"""

def _src_to_array(src: str) -> np.ndarray:
    line_list = src.splitlines(True)
    value_list = _map(lambda l: _map(ord, l), line_list)
    cols = max(len(v) for v in value_list)
    padded_list = _map(lambda v: v + [ord(' ')] * (cols - len(v)), value_list)
    array = np.array(padded_list, dtype=np.uint8)
    return array

def _array_to_src(array: np.ndarray) -> str:
    value_list = array.tolist()
    line_list = _map(lambda v: ''.join(_map(chr, v)), value_list)
    stripped_list = _map(lambda l: l.rstrip(' '), line_list)
    src = ''.join(stripped_list)
    return src

def _map(f, lst: list) -> list:
    return list(map(f, lst))

def srcpic(input: str, output: str, reverse: bool):
    if reverse:
        pic = Image.open(input)
        array = np.asarray(pic)
        src = _array_to_src(array)
        with open(output, 'w') as file:
            file.write(src)
        return src
    else: 
        with open(input) as file:
            src = file.read()
        array = _src_to_array(src)
        pic = Image.fromarray(array)
        pic.save(output)
        return array

def main():
    args = docopt(_cli, version=f'{_name} {_version}')
    srcpic(args['<input>'], args['<output>'], args['--reverse'])

if __name__ == '__main__':
    main()