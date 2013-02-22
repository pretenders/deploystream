deploystream
============

Track the progress of feature development across repositories gathering
information from a multitude of sources.


Running the server locally
--------------------------

``python runserver.py``


Contributing - writing a provider
---------------------------------

There are three different types of provider that can be written for
deploystream. Each have different expectations of what functions they need to
provide and what values they return.

1. Management Provider - see providers/template_management.py

2. Source Code Control Provider - see providers/template_source_code_control.py

3. CI Provider - see providers/template_ci.py


Configuration
-------------

Defining which providers to use
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _configure_provider:

Configuring a provider
~~~~~~~~~~~~~~~~~~~~~~

