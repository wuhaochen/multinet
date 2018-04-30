#!/usr/bin/env python

from setuptools import setup

packages = ['multinet', 'multinet.util']
package_dir = {'multinet': 'multinet', 'multinet.util': 'multinet/util'}

if __name__ == '__main__':

    setup(name='Multinet',
          version='0.01',
          description = 'Networkx extension for multiplex networks',
          author='Haochen Wu',
          author_email='multinet@haochenwu.com',
          packages=packages,
          package_dir=package_dir,
          install_requires=['networkx','dit']
    )
