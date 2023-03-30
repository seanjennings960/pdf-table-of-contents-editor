from typing import Optional
from pathlib import Path

import click



class ParsingError(Exception):
    pass

# def num_tabs(s, tab_size):
#     """number of tabs that fit into a string of length ``s``."""
#     return s // tab_size + 1

class Bookmark:
    def __init__(self, name: str, page_no: int):
        self.name = name
        self.page_no = page_no

    @classmethod
    def from_line(cls, a: str) -> Optional['Bookmark']:
        """Split the line ``a`` into its (name, page)"""
        words = a.rstrip().split(' ')
        if len(words) == 1:
            if not words[0]:
                return None
            else:
                raise ParsingError(f'Found line without page number: {a}')
        try:
            page_no = int(words[-1])
        except ValueError as e:
            raise ParsingError(
                f'Unable to parse page no from string: {repr(a)}') from e
        return Bookmark(' '.join(words[:-1]), page_no)

    def format(self, offset: int = 0):
        return self.name + ' ' + str(self.page_no + offset) + '\n'
    

    # def format_tabs(self, max_length: int, tab_size: int = 4, extra_tabs: int = 3):
    #     # (6 tabs)
    #     # longest string possible
    #     # |   |   |   |   |   |   |
    #     # (4 tabs)
    #     # shorter string  |   |   |
    #     #                         start_i = tab
    #     # To each string append L_longest - L current + 1 tabs
    #     # to get to first unshared space

    #     tabs_to_append = (num_tabs(max_length, tab_size)
    #                       - num_tabs(len(self.name), tab_size) + 1 + extra_tabs)

    #     return self.name + '\t' * tabs_to_append + str(self.page_no) + '\n'


@click.command(help=
    'Output a new table of contents file with page numbers offset.'
    '\n\n'
    'Because oftentimes PDF documents have initial pages which are not '
    'considered in the table of contents page count (e.g. roman numeral-numbered '
    'pages), this script adds an offset to page numbers in a table of contents file '
    'created by the python script "extract_contents" and consumed by '
    'HandyOutliner program')
@click.argument('filename', type=click.Path(exists=True),
                required=True)
@click.option('-s', '--start', type=int, default=0,
              help='The index of the first index for which offset will '
              'be applied. Note that empty lines are disregarded.')
@click.option('-n', '--offset', type=int, required=True,
              help='Number of pages to offset page number between input and output.'
              'files.')
def main(filename: click.Path, offset, start):
    with open(filename, 'r') as f:
        lines = [Bookmark.from_line(l) for l in f.readlines()]
    bookmarks = [l for l in lines if l is not None]
    out_lines = [b.format(offset) if i >= start else b.format()
                 for i, b in enumerate(bookmarks)]
    print(f'Found {len(bookmarks)} bookmarks out of {len(lines)} lines.')
    filename = Path(filename)
    out_name = filename.with_name(filename.stem + '_out' + filename.suffix)
    with open(out_name, 'w') as f:
        f.writelines(out_lines)
    print(f'{out_name} successfully written.')




if __name__ == '__main__':
    main()