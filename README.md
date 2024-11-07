# pyzza

> *Copyright 2023 [piledge]. Licensed under the MIT license.*

`pyzza` is a small collection of Python-Functions created by a Pizza-enthusiast and with no specific topic.

This package is a result of me constantly breaking the DRY principle by copy-and-pasting stuff from old projects into new ones and to have a centralized database to access the functions from several computing instances.

The `pyzza`-package does not solve any large problem, but it can help to save time by eliminating repetitive code and provide easy access to some more complicated interfaces of different packages.

This package is constantly being expanded and improved. Any ideas for new functions or bug reports will be appreciated.


Installing the package
-----------------------

Packages can only be imported if they are located in a directory on the PYTHONPATH (which you can view in python using ``sys.path()``).

Packages installed using the command line tool ``pip`` are added to this path.
This is preferable to manually adding paths to ``sys.path`` in your scripts.
You can install local packages that you are working on in develop mode, by pointing pip the **directory** that contains `setup.py` and your package folder:

    pip install -e local_path/pyzza

This creates a temporary reference to your local package files - you'll see an `.egg-info` file has been created next to your package.
When packages are installed without the ``-e`` flag, they're installed in `site-packages` next to your python installation.

To import pyzza in your Python-Project, simply

    import pyzza


You can also uninstall pyzza once you've finished - don't delete the `.egg-info` reference.
Use the name of the package when deleting it, like so:

    pip uninstall pyzza
