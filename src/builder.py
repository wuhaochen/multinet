"""Build Multinet instance from csv file.

"""
import networkx as nx
import csv

from Multinet import Multinet
import util

def multinet_from_csv(
        file_name,
        filter_func=util.default_filter,
        weight_func=util.default_weight,
        layer_func=util.default_layer,
        ow='ORIGIN',dw='DEST',
        csv_style=''):
    """Build Multinet from csv files.

    Parameters:
    -----------
    filename: str
      The path to csv file.

    filter_func: func
      A function takes line description and a line from the csv file and return a bool. See util/filter_helper for detail.

    weight_func: func or str
      A function takes line description and a line from the csv file and return a number. See util/weight_helper for detail.

    layer_func: func or str
      A function takes line description and a line from the csv file and return a str. See util/layer_helper for detail.

    ow, dw: str
      The key to get nodes name.

    csv_style: str
      style of the csv file.
    
    """
    index_dict = {}
    mg = Multinet()

    if type(weight_func) == str:
        weight_func = util.weight_from_string(weight_func)

    if type(layer_func) == str:
        layer_func = util.layer_from_string(layer_func)
        
    with open(file_name) as netfile:
        if csv_style == 'N':
            netreader = csv.reader(netfile,delimiter=',',quotechar='\"')
        else:
            netreader = csv.reader(netfile,delimiter=',',quotechar='\"',quoting=csv.QUOTE_NONNUMERIC)
        index_line = netreader.next()

        index = 0
        for item in index_line:
            index_dict[item] = index
            index += 1

        origin_index = index_dict[ow]
        dest_index = index_dict[dw]

        for line in netreader:
            if not filter_func(index_dict,line):
                continue

            origin = line[origin_index]
            dest = line[dest_index]
            
            layer = layer_func(index_dict,line)
            weight = weight_func(index_dict,line)
            
            mg.add_node(origin)
            mg.add_node(dest)

            mg.aggregate_edge(origin,dest,layer,weight)

    return mg