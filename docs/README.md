# Documentation

We automatically generate our documentation with a tool called [Sphinx](http://www.sphinx-doc.org/en/master/).

A Sphinx extension, called [sphinx-apidoc](http://www.sphinx-doc.org/en/stable/man/sphinx-apidoc.html),
automatically generates Sphinx sources as reStructuredText or `.rst` files from the code.

For a primer on reStructuredText (rst) view Sphinx's [reStructuredText Primer](http://www.sphinx-doc.org/en/stable/rest.html#rst-primer).

We then post-process reStructuredText with a python script called `prettify_doc.py` which:

    * Moves the *Module Contents" section to the top.
    * And removes headers for "Module Contents", "Submodules" and "Subpackages",
      including their underlines and the following blank line.

Finally, the HTML and other necessary components are built with Sphinx.

We host our documentation with a free service called [Read the Docs](https://readthedocs.org/).

## How to Update the Docs

Make your desired changes.

Then run the bash script:

`./docs/make_docs`

This will do the following:

1. Generate reStructuredText from the `song_match` package with `sphinx-apidoc`.
2. Post-process the reStructuredText files with `prettify_doc.py`.
3. Run `make html` to output the HTML and other necessary files in the `docs/_build` directory.

Verify your changes by opening `docs/_build/html/index.html` in your favorite web browser.

Commit and push your changes.

Read the Docs will then update the docs upon pushing your changes to the repository.
