# Documentation

We automatically generate our documentation with a tool called [Sphinx](http://www.sphinx-doc.org/en/master/).

A Sphinx extension, called [sphinx-apidoc](http://www.sphinx-doc.org/en/stable/man/sphinx-apidoc.html),
automatically generates Sphinx sources as `.rst` files from the code.

We then post-process these `.rst` files with a python script called `prettify_doc.py`.

Finally, the HTML and other necessary components are built with Sphinx.

We host our documentation with a free service called [Read the Docs](https://readthedocs.org/).

## How to Update the Docs

Run the bash script:

`./docs/make_docs`

This will do the following:

1. Generate `.rst` files with `sphinx-apidoc`.
2. Post-process the `.rst` with `prettify_docy.py`.
3. Run `make html` to make the HTML and other necessary files for the website.

Read the Docs will update the docs upon pushing changes to the repository.