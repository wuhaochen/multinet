#!/usr/bin/python

from airnet import *
from helper import *
from measures import *
from filters import *
from weight import *

def number_of_edge_of_new_airport(carrier,start=1999,end=2014,trace = False):
    dict_l = []
    for year in range(start,end):
        airfile_name = default_path+'/T'+str(year)+'.csv'
        for month in range(1,13):
            dest_d = {}
            filt_r = regular_filter()
            filt_s = build_and_filter(CARRIER=carrier,MONTH=month)
            filt = combine_filters_and(filt_s,filt_r)
            weight = weight_from_string('PASSENGERS')
            g = build_airgraph(airfile_name,filt,weight)
            for node in g.vs:
                dest_d[node['name']] = node.outdegree()
            dict_l.append(dest_d)
        if trace:
            print year

    first_appearance = {}
    nl = []

    for key in dict_l[0]:
        first_appearance[key] = (0,dict_l[0][key])

    for i in range(len(dict_l)-1):
        od = dict_l[i]
        nd = dict_l[i+1]
        for key in nd:
            if not od.has_key(key):
                nl.append(nd[key])
            if not first_appearance.has_key(key):
                first_appearance[key] = (i+1,nd[key])

    return first_appearance

def count_new(d):
    return len(filter(lambda x:x[1][0],d.items()))
