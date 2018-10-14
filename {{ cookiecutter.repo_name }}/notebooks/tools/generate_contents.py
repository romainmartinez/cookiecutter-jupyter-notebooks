from pathlib import Path
from operator import itemgetter

import re
import nbformat
from nbformat.v4.nbbase import new_markdown_cell
import yaml

NOTEBOOK_DIR = Path.cwd() / ".."
CONFIG_FILE = NOTEBOOK_DIR / ".." / "config.yml"

REG = re.compile(r'(\d\d)\.(\d\d)-(.*)')

INDEX_COMMENT = "<!--INDEX_COMMENT-->\n"


def get_config(conf, keys):
    with open(conf, 'r') as stream:
        data_loaded = yaml.load(stream)
    return itemgetter(*keys)(data_loaded)


def iter_notebooks():
    return sorted(nb for nb in NOTEBOOK_DIR.glob("*.ipynb") if REG.match(nb.stem))


def get_notebook_title(nb_file):
    nb = nbformat.read(str(nb_file), as_version=4)
    for cell in nb.cells:
        if cell.source.startswith('#'):
            return cell.source[1:].splitlines()[0].strip()


def gen_contents(directory=None):
    for nb in iter_notebooks():
        if directory:
            nb_url = Path(directory) / nb.stem
        else:
            nb_url = nb.resolve()
        chapter, section, title = REG.match(nb.stem).groups()
        title = get_notebook_title(nb)
        if section == '00':
            yield f'\n### [{int(chapter)}. {title}]({nb_url})'
        else:
            yield f"- [{title}]({nb_url})"


def print_contents(directory=None):
    return '\n'.join(gen_contents(directory))


def update_index():
    nb_name = NOTEBOOK_DIR / 'Index.ipynb'

    nb = nbformat.read(str(nb_name), as_version=4)

    is_comment = lambda cell: cell.source.startswith(INDEX_COMMENT)

    if is_comment(nb.cells[-1]):
        print(f'- amending index for {nb_name.stem}')
        nb.cells[1].source = print_contents()
    else:
        print(f'- inserting index for {nb_name.stem}')
        md_cell = f"{INDEX_COMMENT}{print_contents()}"
        nb.cells.append(new_markdown_cell(md_cell))
    nbformat.write(nb, str(nb_name))


if __name__ == '__main__':
    update_index()
    print('if you want to put a ToC in `README.md`:')
    NBVIWER_LINK = get_config(CONFIG_FILE, keys=['nbviewer_link'])
    print(print_contents(NBVIWER_LINK))
