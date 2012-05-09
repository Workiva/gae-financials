GAE Framework
=============


Installation
------------

Install app dependencies: ::

    $ pip install .

Install Node.js (this is for compiling coffeescript and less): ::

    http://nodejs.org/#download

Install node packages: ::

    $ sh node_packages.sh



Development
-----------

Once everything is installed you can now compile the app and go into dev watch mode.
- In this mode you can edit your coffeescript and less files and it will auto compile them for you for easy development. ::

    $ fab dev


To run the local server: ::

    $ fab run
or ::

    $ fab run:args=-p8888
