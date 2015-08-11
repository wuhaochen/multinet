#!/usr/bin/python

# This file contains a series of filter builders that can build filters which are used as parameter of the build_airgraph function.

# Return a filter filt the line satisfies all the simple conditions.
def build_and_filter(**condition):
    def filter_func(index_dict,line):
        for key in condition:
            index = index_dict[key]
            if line[index] != condition[key]:
                return False
        return True
    return filter_func

def build_nand_filter(**condition):
    def filter_func(index_dict,line):
        for key in condition:
            index = index_dict[key]
            if line[index] == condition[key]:
                return False
        return True
    return filter_func

def build_in_and_filter(**condition):
    def filter_func(index_dict,line):
        for key in condition:
            index = index_dict[key]
            if not line[index] in condition[key]:
                return False
        return True
    return filter_func

def combine_filters_and(*filters):
    def filt_func(index_dict,line):
        ret = True
        for filt in filters:
            ret = ret and filt(index_dict,line)
        return ret
    return filt_func

def combine_filters_or(*filters):
    def filt_func(index_dict,line):
        ret = False
        for filt in filters:
            ret = ret or filt(index_dict,line)
        return ret
    return filt_func

def combine_filters_not(filt):
    return lambda i,l:not filt(i,l)

def build_either_in_filter(List):
    return combine_filter_or(build_in_and_filter(ORIGIN=List),build_in_and_filter(DEST=List))

def build_both_in_filter(List):
    return build_in_and_filter(ORIGIN=List,DEST=List)

def regular_filter():
    filt_class = build_and_filter(CLASS='F')
    filt_scheduled = build_nand_filter(DEPARTURES_SCHEDULED=0.0)
    filt_passenger = build_nand_filter(PASSENGERS=0.0)
    return combine_filters_and(filt_class,filt_scheduled,filt_passenger)

def cargo_filter():
    filt_performed = build_nand_filter(DEPARTURES_PERFORMED=0.0)
    return combine_filters_and(filt_performed)