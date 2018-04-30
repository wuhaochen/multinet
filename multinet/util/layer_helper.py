"""Utility function to build a layer_func used by builder.

layer_func should take two arguments.
  The first argument is a dict describe the csv file.
    The key of the dict is field name for csv file.
    The value of the dict is field index for csv file.
  The second argument is a list represent a line in csv file.
layer_func should return a str as the layer name.
"""

default_layer = lambda x,y:"Default_layer"

def layer_from_string(layer_s):
    def layer_func(index_dict,line):
        l = index_dict[layer_s]
        return line[l]
    return layer_func

def layer_comtrade(aggregation=0):
    def layer_func(index_dict,line):
        l = index_dict['hs6']
        code = line[l]
        return str(int(code/(10**aggregation)))
    return layer_func

def layer_icews(dlevel=2):
    def layer_func(index_dict,line):
        l = index_dict['CAMEO Code']
        code = line[l]
        return code[:dlevel]
    return layer_func