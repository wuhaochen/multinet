#!/usr/bin/python

def g_katrina():
    airfile = default_path + 'T2005.csv'
    filt8 = build_and_filter(MONTH='8',CLASS='F')
    filt9 = build_and_filter(MONTH='9',CLASS='F')
    weight = weight_from_string('PASSENGERS')

    g8 = build_airgraph(airfile,filt8,weight)
    g9 = build_airgraph(airfile,filt9,weight)

    return [g8,g9]
