#!/usr/bin/env python

from distutils.core import setup

packages = ['multinet']
package_dir = {'multinet': 'src'}

if __name__ == '__main__':

    setup(name='Multinet',
          version='0.01',
          description = 'Networkx extension for multiplex networks',
          author='Haochen Wu',
          author_email='multinet@haochenwu.com',
          packages=packages,
          package_dir=package_dir
    )

