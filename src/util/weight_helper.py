default_weight = lambda x,y:1.0

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
        source = line[origin]
        target = line[dest]
        try:
            ref_w = ref_g[source][target]['weight']
        except:
            ref_w = 0
        if ref_w != 0:
            return float(line[w])/ref_w
        else:
            return 0
    return weight_func
