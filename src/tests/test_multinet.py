"""
Test the Multinet Class.
"""
from nose.tools import *
import multinet as mn

def test_build_multinet():
    """
    Test building Multinet objects.
    """
    mg = mn.Multinet()
    mg.add_edge(0,1,'L1')
    mg.add_edge(1,2,'L2')

    assert_equal(mg.number_of_nodes(),3)
    assert_equal(mg.number_of_edges(),2)
    assert_equal(mg.number_of_layers(),2)

    mg.remove_edge(0,1)
    assert_equal(mg.number_of_nodes(),3)
    assert_equal(mg.number_of_edges(),1)
    assert_equal(mg.number_of_layers(),2)

    mg.remove_empty_layers()
    assert_equal(mg.number_of_layers(),1)
