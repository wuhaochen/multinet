import util
import builder
import networkx as nx

from params import default_path

def mg_by_year(year):
    airfile = default_path + 'T' + str(year) + '.csv'
    filt = util.regular_filter()
    weightf = util.weight_from_string('PASSENGERS')
    layerf = util.layer_from_string('CARRIER')
    return builder.multinet_from_csv(airfile,filt,weightf,'CARRIER')

def trimed_mg_by_year(year):
    mg = mg_by_year(year)
    c = list(nx.strongly_connected_components(mg))
    c = sorted(c,key=len,reverse=True)
    to_remove = set(mg.nodes())-set(c[0])
    mg.remove_nodes_from(to_remove)
    mg.remove_empty_layers()
    return mg