deploystream
============

Track the progress of feature development across repositories gathering
information from a multitude of sources.

Getting started
---------------

You'll need to create a ``github_auth.py`` file with an application's APP_ID
and APP_SECRET from github.

These are used to represent deploystream as an application that will be granted
access to your own GitHub account.

Alter the configuration of GITHUB_CONFIG in local_settings.py to point to the
repo of choice.

Running the server locally
--------------------------

``CONFIG=<config_name> ./scripts/runserver.sh``

Where config_name is found in a file named:

    ``config/local_settings_<config_name>.py``


Running the tests
-----------------

``CONFIG=test nosetests``

or

``./scripts/tests``


Contributing - writing a provider
---------------------------------

There are three different types of provider that can be written for
deploystream. Each have different expectations of what functions they need to
provide and what values they return.

1. Management Provider - see providers/examples/template_management.py

2. Source Code Control Provider - see providers/examples/template_source_code_control.py

3. CI Provider - see providers/examples/template_ci.py


Configuration
-------------

Defining which providers to use
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _configure_provider:

Configuring a provider
~~~~~~~~~~~~~~~~~~~~~~


