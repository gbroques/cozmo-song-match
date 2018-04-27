Virtual Environments
====================

The following document addresses what a virtual environment is, and how to set one up.

What Is a Virtual Environment?
------------------------------
To explain what a virtual environment is, and why it's needed, consider the following example:

You have two projects, **A** and **B**. Both depend on different versions of the same library.

* Project A requires version **1.12.4**.
* And Project B requires version **2.5.6**.

How do you manage this?

The solution is to create an isolated *virtual environment* for each project.

``virtualenv`` is a tool to create isolated Python environments.

How to Setup a Virtual Environment
----------------------------------
The following are steps to setup a virtual environment for the Song Match project.

1. `Install virtualenv <https://virtualenv.pypa.io/en/stable/installation/>`_
2. Navigate to the root of the Song Match repository on your machine.

::

$ cd path/to/song/match/repo

.. Note:: See `Setup <setup>`_ for how to clone the repository.

3. Create the virtual environment. We'll call it ``venv``, but you can call it anything.

::

$ virtualenv venv

4. Activate the virtual environment. This step depends upon your operating system. See
`activate script <https://virtualenv.pypa.io/en/stable/userguide/#activate-script>`_ for details.

For **POSIX** based systems:

::

$ source venv/bin/activate

For **Windows**:

::

> venv\Scripts\activate

5. Install the project's requirements.

::

$ pip install -r requirements.txt

6. You can deactivate the virtual environment at anytime with the command:

::

$ deactivate

.. Error:: Having Trouble? See `virtualenv's documentation <https://virtualenv.pypa.io/en/stable/#>`_ for help.