PyCharm
=======

This document aims to explain why we recommend using PyCharm to develop Song Match.

If you haven't already, download and install PyCharm Community Edition `here <https://www.jetbrains.com/pycharm/download/>`_.

Finding Usages
--------------

The first reason we recommend you use PyCharm is the ability to
`find usages <https://www.jetbrains.com/help/pycharm/finding-usages.html>`_.
Often when developing you need to find all the places where a function is called. PyCharm makes this easy.

For example, here's a function that checks for whether the game is over in ``song_match.py``.

.. image:: /_static/check-for-game-over.png

If you hover over the name of the function while holding :kbd:`Ctrl`,
and click the name of the function you can find usages.

PyCharm also has other keyboard shortcuts and ways to find usages that are helpful to learn.

.. image:: /_static/find-usages.png

The tooltip window shows the function is called in two places:

1. Line ``98`` in ``song_match.py``
2. and line ``117`` in ``song_match.py``

You can select either usage and PyCharm will automatically navigate there for you.

.. Note:: Finding usages works for functions, methods, variables, and anything else you could care about.

Enforcing PEP 8
---------------

PyCharm also helps developers follow Python's official style guide PEP 8.

For example, PEP 8 says variables should use snake case instead of camel case.

.. image:: /_static/enforcing-pep8.png

PyCharm underlines the camelcase variable with a yellow squiqqly line
and suggests renaming it from ``numPlayers`` to ``num_players``.

So Much More
------------

PyCharm offers many other great features that are outside the scope of this document like:

* Integration with ``requirements.txt`` files
* Powerful refactoring abilities
* Automatic optimizing of imports and reformatting
* and so much more.

You can find more information on `JetBrain's website <https://www.jetbrains.com/help/pycharm/meet-pycharm.html>`_.