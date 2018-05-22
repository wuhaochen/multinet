multinet
========

|build| |codecov|

multinet is a networkx extension to handle multiplex network. It contains some useful function to handle operations that specific to multiplex network and it's still pretty much compatible with networkx functions as the aggregated network.

It is currently still in progress.

Install
-------
Install from the source::

    $  pip install .

Simple Example
--------------
A two layer multiplex network::

   >>> import multinet as mn
   >>> mg = mn.MultiNet()
   >>> mg.add_node(1)
   >>> mg.add_node(2)
   >>> mg.add_edge(1, 2, 'Layer_1')
   >>> mg.add_edge(1, 2, 'Layer_2')
   >>> mg.number_of_layers()
   2

.. |build| image:: https://travis-ci.org/wuhaochen/multinet.svg?branch=master
   :target: https://travis-ci.org/wuhaochen/multinet
   :alt: Continuous Integration Status
   
.. |codecov| image:: https://codecov.io/gh/wuhaochen/multinet/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/wuhaochen/multinet
   :alt: Code Coverage Status
