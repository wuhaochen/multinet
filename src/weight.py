#!/usr/bin/python

def weight_from_string(weight_s):
    def weight_func(index_dict,line):
        w = index_dict[weight_s]
        return float(line[w])
    return weight_func

def weight_from_ratio(ref_g,weight_s):
    def weight_func(index_dict,line):
        w = index_dict[weight_s]
        origin = index_dict['ORIGIN']
        dest = index_dict['DEST']
        source = ref_g.vs.find(line[origin])
        target = ref_g.vs.find(line[dest])
        try:
            eid = ref_g.get_eid(source.index,target.index)
            ref_w = ref_g.es[eid]['weight']
        except:
            ref_w = 0
        if ref_w != 0:
            return float(line[w])/ref_w
        else:
            return 0
    return weight_func
