import nbformat

from generate_contents import iter_notebooks, NOTEBOOK_DIR


def fix_kernelspec():
    for nb_name in iter_notebooks():
        nb = nbformat.read(str(nb_name), as_version=4)

        print(f"- Updating kernelspec for {nb_name.stem}")
        nb['metadata']['kernelspec']['display_name'] = 'Python 3'

        nbformat.write(nb, str(nb_name))


if __name__ == '__main__':
    fix_kernelspec()
