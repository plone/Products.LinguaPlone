Development
===========

This is the development buildout for LinguaPlone itself. It is not meant for
anything else. It is not an example on how to run anything in production.

If you want look into virtual hosting issues, there is an extra buildout
configuration file ``nginx.cfg`` which makes this rather simple.

Run::

  bin/buildout -c nginx.cfg

Then you can start an instance and a nginx web server::

  bin/instance start
  sh bin/nginx.sh

You can now access the ZMI on ``127.0.0.1:8080``. Create a Plone site with the
id ``Plone`` and choose to install LinguaPlone from the available add-ons.

To access the site with virtual hosting enabled, use ``127.0.0.1:8000``.
