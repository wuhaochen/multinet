#!/usr/bin/python

import igraph
import sys
import csv

airnet = igraph.Graph(directed=True)

def correlation_pairs(g1,g2):
    for node in g1.vs:
        try:
            g2.vs.find(node['name'])
        except:
            g2.add_vertex(node['name'])
    for node in g2.vs:
        try:
            g1.vs.find(node['name'])
        except:
            g1.add_vertex(node['name'])

    g1_weight_sum = 0.0
    g2_weight_sum = 0.0

    for edge in g1.es:
        g1_weight_sum += edge['weight']
    for edge in g2.es:
        g2_weight_sum += edge['weight']

    g1_weight_avg = g1_weight_sum/pow(len(g1.vs),2)
    g2_weight_avg = g2_weight_sum/pow(len(g2.vs),2)

    cov_sum = 0.0
    g1_weight_dev_sum = 0.0
    g2_weight_dev_sum = 0.0

    for source in g1.vs:
        for target in g1.vs:
            w1 = 0.0
            w2 = 0.0
            try:
                eid = g1.get_eid(source.index,target.index)
                w1 = g1.es[eid]['weight']
            except:
                pass
            try:
                eid = g2.get_eid(source.index,target.index)
                w2 = g2.es[eid]['weight']
            except:
                pass
            cov_sum += (w1-g1_weight_avg)*(w2-g2_weight_avg)
            g1_weight_dev_sum += pow((w1-g1_weight_avg),2)
            g2_weight_dev_sum += pow((w2-g1_weight_avg),2)

    correlation = cov_sum/pow((g1_weight_dev_sum*g2_weight_dev_sum),0.5)
    return correlation

def correlation_common(g1,g2):
    for node in g1.vs:
        try:
            g2.vs.find(node['name'])
        except:
            g2.add_vertex(node['name'])
    for node in g2.vs:
        try:
            g1.vs.find(node['name'])
        except:
            g1.add_vertex(node['name'])

    g1_weight_sum = 0.0
    g2_weight_sum = 0.0
    common_edge_count = 0

    for edge in g1.es:
        source = g2.vs.find(g1.vs[edge.source]['name'])
        target = g2.vs.find(g1.vs[edge.target]['name'])
        try:
            eid = g2.get_eid(source.index,target.index)
            common_edge_count += 1
            g1_weight_sum += edge['weight']
            g2_weight_sum += g2.es[eid]['weight']
        except:
            pass

    g1_weight_avg = g1_weight_sum/common_edge_count
    g2_weight_avg = g2_weight_sum/common_edge_count

    cov_sum = 0.0
    g1_weight_dev_sum = 0.0
    g2_weight_dev_sum = 0.0

    for edge in g1.es:
        source = g2.vs.find(g1.vs[edge.source]['name'])
        target = g2.vs.find(g1.vs[edge.target]['name'])
        try:
            eid = g2.get_eid(source.index,target.index)
            w1 = edge['weight']
            w2 = g2.es[eid]['weight']
            cov_sum += (w1-g1_weight_avg)*(w2-g2_weight_avg)
            g1_weight_dev_sum += pow((w1-g1_weight_avg),2)
            g2_weight_dev_sum += pow((w2-g1_weight_avg),2)
        except:
            pass

    correlation = cov_sum/pow((g1_weight_dev_sum*g2_weight_dev_sum),0.5)
    return correlation

def correlation_either(g1,g2):
    for node in g1.vs:
        try:
            g2.vs.find(node['name'])
        except:
            g2.add_vertex(node['name'])
    for node in g2.vs:
        try:
            g1.vs.find(node['name'])
        except:
            g1.add_vertex(node['name'])

    for edge in g1.es:
        source = g2.vs.find(g1.vs[edge.source]['name'])
        target = g2.vs.find(g1.vs[edge.target]['name'])
        try:
            eid = g2.get_eid(source.index,target.index)
        except:
            g2.add_edge(source,target,weight=0)

    for edge in g2.es:
        source = g1.vs.find(g2.vs[edge.source]['name'])
        target = g1.vs.find(g2.vs[edge.target]['name'])
        try:
            eid = g1.get_eid(source.index,target.index)
        except:
            g1.add_edge(source,target,weight=0)

    g1_weight_sum = 0.0
    g2_weight_sum = 0.0

    for edge in g1.es:
        source = g2.vs.find(g1.vs[edge.source]['name'])
        target = g2.vs.find(g1.vs[edge.target]['name'])
        eid = g2.get_eid(source.index,target.index)
        g1_weight_sum += edge['weight']
        g2_weight_sum += g2.es[eid]['weight']

    g1_weight_avg = g1_weight_sum/len(g1.es)
    g2_weight_avg = g2_weight_sum/len(g2.es)

    cov_sum = 0.0
    g1_weight_dev_sum = 0.0
    g2_weight_dev_sum = 0.0

    for edge in g1.es:
        source = g2.vs.find(g1.vs[edge.source]['name'])
        target = g2.vs.find(g1.vs[edge.target]['name'])
        eid = g2.get_eid(source.index,target.index)
        w1 = edge['weight']
        w2 = g2.es[eid]['weight']
        cov_sum += (w1-g1_weight_avg)*(w2-g2_weight_avg)
        g1_weight_dev_sum += pow((w1-g1_weight_avg),2)
        g2_weight_dev_sum += pow((w2-g1_weight_avg),2)

    correlation = cov_sum/pow((g1_weight_dev_sum*g2_weight_dev_sum),0.5)
    return correlation

def main(argv):
    airfile_name = argv[1]

    index_dict = {}
#    airnet = igraph.Graph(directed=True)

    with open(airfile_name) as airfile:
        airreader = csv.reader(airfile,delimiter=',',quotechar='\"')
        index_line = airreader.next()

        index = 0
        for item in index_line:
            index_dict[item] = index
            index += 1

        origin = index_dict['ORIGIN']
        dest = index_dict['DEST']
        dp = index_dict['DEPARTURES_PERFORMED']
        passenger = index_dict['PASSENGERS']
        carrier = index_dict['CARRIER']
        config = index_dict['AIRCRAFT_CONFIG']
        rank = index_dict['CLASS']

        for line in airreader:
            if line[config] != '1' or line[rank] != 'F':
                continue
            try:
                airnet.vs.find(line[origin])
            except:
                airnet.add_vertex(line[origin])
            try:
                airnet.vs.find(line[dest])
            except:
                airnet.add_vertex(line[dest])

            source = airnet.vs.find(line[origin])
            target = airnet.vs.find(line[dest])
            try:
                airnet.get_eid(source.index,target.index)
            except:
                airnet.add_edge(source,target,weight=0)
            
            eid = airnet.get_eid(source.index,target.index)
            airnet.es[eid]['weight'] += float(line[dp])

        airnet.vs["label"] = airnet.vs["name"]
        igraph.plot(airnet)
        
if __name__ == "__main__":
    main(sys.argv)
