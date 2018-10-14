import itertools

import nbformat
from nbformat.v4.nbbase import new_markdown_cell

from generate_contents import CONFIG_FILE, iter_notebooks, get_notebook_title, get_config


def prev_this_next(it):
    a, b, c = itertools.tee(it, 3)
    next(c)
    return zip(itertools.chain([None], a), b, itertools.chain(c, [None]))


PREV_TEMPLATE = "< [{title}]({url}) "
CONTENTS = "| [Contents](Index.ipynb) |"
NEXT_TEMPLATE = " [{title}]({url}) >"
NAV_COMMENT = "<!--NAVIGATION-->\n"

COLAB_LINK = """
<a href="{colab_link}/{notebook_filename}">\
<img align="left" src="https://colab.research.google.com/assets/colab-badge.svg" \
alt="Open in Colab" title="Open and Execute in Google Colaboratory"></a>
"""


def iter_navbars():
    for prev_nb, nb, next_nb in prev_this_next(iter_notebooks()):
        navbar = NAV_COMMENT
        if prev_nb:
            navbar += PREV_TEMPLATE.format(title=get_notebook_title(prev_nb),
                                           url=prev_nb.parts[-1])
        navbar += CONTENTS
        if next_nb:
            navbar += NEXT_TEMPLATE.format(title=get_notebook_title(next_nb),
                                           url=next_nb.parts[-1])

        colab_link = get_config(CONFIG_FILE, keys=['colab_link'])
        navbar += COLAB_LINK.format(colab_link=colab_link, notebook_filename=nb.parts[-1])
        yield nb, navbar


def write_navbars():
    for nb_name, navbar in iter_navbars():
        nb = nbformat.read(str(nb_name), as_version=4)
        is_comment = lambda cell: cell.source.startswith(NAV_COMMENT)

        if is_comment(nb.cells[1]):
            print(f"- amending navbar for {nb_name.stem}")
            nb.cells[1].source = navbar
        else:
            print(f"- inserting navbar for {nb_name.stem}")
            nb.cells.insert(1, new_markdown_cell(source=navbar))

        if is_comment(nb.cells[-1]):
            nb.cells[-1].source = navbar
        else:
            nb.cells.append(new_markdown_cell(source=navbar))
        nbformat.write(nb, str(nb_name))


if __name__ == '__main__':
    write_navbars()
