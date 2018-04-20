"""
Test the Multinet Class.
"""
import pytest
import multinet as mn

def test_build_multinet():
    """
    Test building Multinet objects.
    """
    mg = mn.Multinet()
    mg.add_edge(0,1,'L1')
    mg.add_edge(1,2,'L2')

    assert mg.number_of_nodes() == 3
    assert mg.number_of_edges() == 2
    assert mg.number_of_layers() == 2

    mg.remove_edge(0,1)
    assert mg.number_of_nodes() == 3
    assert mg.number_of_edges() == 1
    assert mg.number_of_layers() == 2

    assert len(mg.empty_layers()) == 1

    mg.remove_empty_layers()

    assert mg.number_of_layers() == 1
