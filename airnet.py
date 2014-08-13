#!/usr/bin/python

import igraph
import sys
import csv

airnet = igraph.Graph(directed=True)

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
