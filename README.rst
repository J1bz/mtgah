Installation
============
Dependencies
------------
Python 3.4+

.. code:: bash
    pip install bottle

Administration
==============
.. code:: bash
    cd /path/to/mtgah
    python mtgah-webapp.py

Usage
=====
Routes :
  - mtgah.domain.pizza/ : Not much to see there
  - mtgah.domain.pizza/[CODE]?r=m,r,u,c : Where [CODE] is the expansion code
    (a list is given in the footer)

Query parameters :
  - r : Which rarities to display (separated by commas). Default is m,r.
