import matplotlib.pyplot as plt
import numpy as np
import json

def get_ticks(start=1999,end=2014):
    # plt.xticks(x, get_ticks(), rotation = 45)
    ticks = []
    for year in range(start,end):
        ticks.append(str(year))
        ticks += [""] * 11
    return ticks

All = json.load(open('../result/all_passengers.json'))
x = range(len(All))
dummy = plt.plot(x,All)
dummy = plt.xticks(x,get_ticks(),rotation=45)
dummy = plt.xlabel('Time')
dummy = plt.gcf().subplots_adjust(bottom=0.15)
dummy = plt.ylabel('Number of passengers')
plt.savefig('../writeup/pic/passengers_all.png')
plt.clf()

top5 = json.load(open('../result/top5_passengers.json'))
x = range(len(top5))
dummy = plt.plot(x,top5)
dummy = plt.xticks(x,get_ticks(),rotation=45)
dummy = plt.xlabel('Time')
dummy = plt.gcf().subplots_adjust(bottom=0.15)
dummy = plt.ylabel('Number of passengers')
plt.savefig('../writeup/pic/passengers_top5.png')
plt.clf()

dummy = plt.plot(x,All,label='All carriers')
dummy = plt.plot(x,top5,label='Top 5 carriers')
dummy = plt.xticks(x,get_ticks(),rotation=45)
dummy = plt.xlabel('Time')
dummy = plt.ylabel('Number of passengers')
dummy = plt.legend()
plt.savefig('../writeup/pic/passengers_all_and_top5.png')
plt.clf()

passenger = json.load(open('../result/passenger.json'))
for carrier in passenger:
    dummy = plt.plot(x,passenger[carrier],label=carrier)
dummy = plt.xticks(x,get_ticks(),rotation=45)
dummy = plt.xlabel('Time')
dummy = plt.gcf().subplots_adjust(bottom=0.15)
dummy = plt.ylabel('Number of passengers')
dummy = plt.ylim(0)
dummy = plt.legend(loc='lower right')
plt.savefig('../writeup/pic/passengers_top5_ind.png')
plt.clf()

passenger_ratio = json.load(open('../result/passenger_ratio.json'))
for carrier in passenger_ratio:
    dummy = plt.plot(x,passenger_ratio[carrier],label=carrier)
dummy = plt.xticks(x,get_ticks(),rotation=45)
dummy = plt.xlabel('Time')
dummy = plt.gcf().subplots_adjust(bottom=0.15)
dummy = plt.ylabel('Market share')
dummy = plt.legend(loc='lower right')
plt.savefig('../writeup/pic/passengers_top5_ratio.png')
plt.clf()

def degree_distribution(deg_seq,filename=None):
    hist,bins = np.histogram(deg_seq,bins=range(max(deg_seq)+1))
    width = 0.7
    center = (bins[:-1] + bins[1:]) / 2
    dummy = plt.bar(center,hist,align='center',width=width)
    dummy = plt.xlabel('Degree')
    dummy = plt.ylabel('Number of nodes')
    if filename:
        plt.savefig(filename)
        plt.clf()
    else:
        plt.show()
    return 0

degrees = json.load(open('../result/degree.json'))
years = [1999,2006,2013]
carriers = ['AA','UA','US','WN','DL']

for year in years:
    for carrier in carriers:
        deg_seq = degrees[str(year)][carrier]
        filename = '../writeup/pic/degree_dist_'+str(year)+'_'+carrier+'.png'
        degree_distribution(deg_seq,filename)

