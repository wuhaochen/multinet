#!/usr/bin/python

def layer_from_string(layer_s):
    def layer_func(index_dict,line):
        l = index_dict[layer_s]
        return line[l]
    return layer_func

def layer_comtrade(aggregation=0):
    def layer_func(index_dict,line):
        l = index_dict['hs6']
        code = line[l]
        return code/(10**aggregation)
    return layer_func