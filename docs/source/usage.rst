Usage
=====

Installation
------------

spsm can be installed using pip:

.. code-block:: console

  (.venv) $ pip install spsm
  (.venv) $ spsm -v
  Simple Python Server Manager, v0.1.2

Quick Start
-----------

1. Create a directory for your server

  .. code-block:: console

    (.venv) $ mkdir my_server
    (.venv) $ cd my_server

2. Initialize the directory

  .. code-block:: console

    (.venv) $ spsm init

3. Add a server jar and apply the new configuration

  .. code-block:: console

    (.venv) $ spsm upsert -u [jar source url] server server_jar
    (.venv) $ spsm jars apply

4. Activate the server wrapper

  .. code-block:: console

    (.venv) $ spsm server activate -a

5. Once in the interactive wrapper terminal, use the command :code:`start` to start the server.
:code:`help` can also be used to list available commands

  .. code-block:: console

    spsm >> start

.. note:: 

  Sometimes the output can be initially off by a line or two depending on the size of the terminal.
  Output can be scrolled up and down using the arrow keys

.. note:: 

  The server will typically not successfully start the first time as you will have to update the 
  :code:`eula.txt`

6. The interactive terminal can be exited without terminating the server using the :code:`exit` command
or by pressing :code:`CTRL+A CTRL+D`

.. seealso:: 

  The wrapper is managed using the :code:`screen` command.
  see `here <https://www.gnu.org/software/screen/manual/screen.html>`_ for more information on screens.

Commands
--------

.. click:: cli.spsm:spsm
  :prog: spsm
  :commands: init,list
  :nested: full

----

.. click:: cli.spsm:server
  :prog: spsm server
  :nested: full

----

.. click:: cli.spsm:jars
  :prog: spsm jars
  :nested: full