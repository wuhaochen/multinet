import util
import builder

from params import default_path

def mg_by_year(year):
    airfile = default_path + 'T' + str(year) + '.csv'
    filt = util.regular_filter()
    weightf = util.weight_from_string('PASSENGERS')
    layerf = util.layer_from_string('CARRIER')
    return builder.multinet_from_csv(airfile,filt,weightf,'CARRIER')
