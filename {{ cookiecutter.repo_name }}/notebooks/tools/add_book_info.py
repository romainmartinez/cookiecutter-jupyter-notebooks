import nbformat
from nbformat.v4.nbbase import new_markdown_cell

from generate_contents import CONFIG_FILE, iter_notebooks, get_config

REPO_COMMENT = "<!--BOOK_INFORMATION-->\n"

REPO_INFO = REPO_COMMENT + get_config(CONFIG_FILE, keys=['repo_info'])


def add_book_info():
    for nb_name in iter_notebooks():
        nb = nbformat.read(str(nb_name), as_version=4)

        is_comment = lambda cell: cell.source.startswith(REPO_COMMENT)

        if is_comment(nb.cells[0]):
            print(f'- amending comment for {nb_name.stem}')
            nb.cells[0].source = REPO_INFO
        else:
            print(f'- inserting comment for {nb_name.stem}')
            nb.cells.insert(0, new_markdown_cell(REPO_INFO))
        nbformat.write(nb, str(nb_name))


if __name__ == '__main__':
    add_book_info()
