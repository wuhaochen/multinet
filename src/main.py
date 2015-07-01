#!/usr/bin/python

from multinet import *
from helper import *
from measures import *
from filters import *
from weight import *
import sys

default_path = '/home/hcwu/data/transtat/'

Katrina = ['0R3','08A','15A','1L0','1R8','2R5','2R7','33J','3M8','4R1','4R4','4R7','4R9','5R2','5R4','5R7','66Y','71J','7A3','8A1','AEX','AIV','ASD','BFM','BIX','BTR','BXA','CWF','GNF','GPT','HBG','HDC','HEZ','HKS','HSA','HSV','HUM','HZR','JAN','JKA','L31','L38','L39','L49','L83','LCH','LFT','M13','M24','MCB','MEI','MJD','MOB','MSL','MSY','NBG','NEW','NMM','PIB','PLR','PQL','PTN','RQR','RSN','SPH','TVR']

KatrinaF = ['MSY', 'JAN', 'MOB', 'BTR', 'GPT', 'LFT', 'HSV', 'AEX', 'MSL', 'LCH', 'PIB', 'MEI']

Carriers = ['WN','DL','UA','AA','US','EV','B6','OO','AS','FL','MQ','9E','NK','YX','F9','HA','YV','G4','QX','VX']

cor89 = 0.34211394938129946

cor1 = []
cor2 = []
cor3 = []
gc = []

focus = {}
focus_in = {}
focus_out = {}

graphs = []

WN = []
DL = []
UA = []
AA = []
US = []

All = []

def main(argv):
    if argv and len(argv) > 1:
        path = argv[1]
    else:
        path = default_path

        '''    for carrier in Carriers:
        focus[carrier] = []
        focus_in[carrier] = []
        focus_out[carrier] = []
        '''

#    airfile_name = path +'/T1998.csv'
    #filt1 = build_and_filter(CARRIER='DL',MONTH=str('12'),CLASS='F')
    #filt2 = build_and_filter(CARRIER='NW',MONTH=str('12'),CLASS='F')
    '''    def filt1(index_dict,line):
        origin = index_dict['ORIGIN']
        dest = index_dict['DEST']
        if line[origin] in Katrina:
            return True
        if line[dest] in Katrina:
            return True
        return False'''

 #   filt1 = lambda x,y:True
 #   filt2 = build_and_filter(MONTH=str('12'),CLASS='F')
 #   filt = lambda x,y:filt1(x,y) and filt2(x,y)
 #   weight = weight_from_string('PASSENGERS')
 #   pg = build_airgraph(airfile_name,filt,weight,True,'CARRIER')

    for year in range(1999,2014):
        airfile_name = path+'/T'+str(year)+'.csv'
        for month in range(1,13):
            #filt1 = build_and_filter(CARRIER='DL',MONTH=str(month),CLASS='F')
            #filt2 = build_and_filter(CARRIER='NW',MONTH=str(month),CLASS='F')
            #airports = []
            print str(year)+' ' +str(month)
            filt_r = regular_filter()
            filt_m = build_and_filter(MONTH = month)
            filt = combine_filters_and(filt_r,filt_m)
            weight = weight_from_string('PASSENGERS')
            #g = build_airgraph(airfile_name,filt,weight,True,'CARRIER')
            g = build_airgraph(airfile_name,filt,weight)
            All.append(count_all(g))
            #reduce_to_degree(g)
            #temp = attach_focus_nodes(g)
            #temp = ['','',count_by_layer(g)]

            #WN.append(temp[2]['WN'])
            #DL.append(temp[2]['DL'])
            #UA.append(temp[2]['UA'])
            #AA.append(temp[2]['AA'])
            #US.append(temp[2]['US'])
            '''for node in gt.vs:
                airports.append(node['name'])

            def filt3(index_dict,line):
                origin = index_dict['ORIGIN']
                dest = index_dict['DEST']
                if not line[origin] in airports:
                    return False
                if not line[dest] in airports:
                    return False
                return True        

            filt = lambda x,y: filt2(x,y) and filt3(x,y)
            g = build_airgraph(airfile_name,filt,weight)'''
            

'''    airfile_name = path+'/T2013.csv'
    carriers = ['WN','DL','UA','AA','US','EV','OO']
    filt = build_and_filter(CLASS='F') 
    weight = weight_from_string('PASSENGERS')
    gf = build_airgraph(airfile_name,filt,weight)
    for carrier in carriers:
        filt = build_and_filter(CARRIER=carrier,CLASS='F')
        weight = weight_from_ratio(gf,'PASSENGERS')
        g = build_airgraph(airfile_name,filt,weight)
        graphs.append(g)

    import copy

    i = 0
    for g1 in graphs:
        cor1.append([])
        cor2.append([])
        cor3.append([])
        for g2 in graphs:
            g1t = copy.copy(g1)
            g2t = copy.copy(g2)
            cor1[i].append(correlation_pairs(g1t,g2t))
            cor2[i].append(correlation_common(g1t,g2t))
            cor3[i].append(correlation_either(g1t,g2t))
        print i
        i = i+1
'''

'''    for year in range(2005,2013):
        airfile_name = path+'/T'+str(year)+'.csv'
        for month in range(1,13):
            filt1 = build_and_filter(CARRIER='NW',MONTH=str(month),CLASS='F')
            filt2 = build_and_filter(CARRIER='DL',MONTH=str(month),CLASS='F')
            filtc = lambda x,y:filt1(x,y) or filt2(x,y)
            weight = weight_from_string('PASSENGERS')
            g = build_airgraph(airfile_name,filt1,weight)
            g.to_undirected()
            temp = gini(g)
            print temp
            gc.append(temp)
'''

'''            filter0 = build_and_filter(MONTH=str(month))
            filter1 = build_and_filter(CARRIER='CO',MONTH=str(month))
            filter2 = build_and_filter(CARRIER='UA',MONTH=str(month))

            weight = weight_from_string('PASSENGERS')
            g = build_airgraph(airfile_name,filter0,weight)

            weight_ratio = weight_from_ratio(g,'PASSENGERS')

            g1 = build_airgraph(airfile_name,filter1,weight)
            g2 = build_airgraph(airfile_name,filter2,weight)

            cp = correlation_pairs(g1,g2)
            print gini(g1)
            cor1.append(cp)
            cc = correlation_common(g1,g2)
            cor2.append(cc)
            ce = correlation_either(g1,g2)
            cor3.append(ce)
'''

if __name__ == "__main__":
    main(sys.argv)
