deploystream
============

Track the progress of feature development across repositories gathering
information from a multitude of sources.

Getting started
---------------

You'll need to create a ``github_auth.py`` file with your TOKEN information from
github.

Do this by running ``get_github_token.py`` and follow the steps. That will
enable access to github. Alter the configuration of GITHUB_CONFIG in
local_settings.py to point to the repo of choice.

Running the server locally
--------------------------

``python runserver.py``


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


