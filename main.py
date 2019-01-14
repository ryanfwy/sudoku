'''CLI entrance.'''

import argparse
import os

parser = argparse.ArgumentParser(prog='sudoku')
parser.add_argument('path', action='store', help='Set the path of image.', type=str)
parser.add_argument('-s', '--source', required=False, action='store_true', help='Show the source matrix.')
parser.add_argument('-t', '--tips', required=False, action='store_true', help='Show the tips.')
parser.add_argument('-a', '--answer', required=False, action='store_true', help='Show the answer.')

args = parser.parse_args()
if args.path:
    if os.path.exists(args.path) == False:
        print('Wrong image path.')
        exit()

    import process

    result = process.run(args.path)

    print()

    if not (args.tips or args.answer) or args.source:
        print('Here is the source matrix:')
        process.show(result)
    if args.tips:
        process.show(result, tips=True)
    if args.answer:
        process.show(result, answer=True)
