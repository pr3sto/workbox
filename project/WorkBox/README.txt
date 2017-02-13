Installation and Setup
======================

Install ``WorkBox`` using the setup.py script::

    $ cd WorkBox
    $ python setup.py develop

Create the workbox database for any model classes defined::

    $ gearbox setup-app

Start the paste http server::

    $ gearbox serve

While developing you may want the server to reload after changes in package files (or its dependencies) are saved. This can be achieved easily by adding the --reload option::

    $ gearbox serve --reload --debug

Then you are ready to go.
