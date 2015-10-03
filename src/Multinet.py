import networkx as nx

class Multinet(nx.DiGraph):
    '''
    Multiplex network class.
    '''
    
    def __init__(self):
        super(self.__class__,self).__init__()
        self.graph['layers'] = []

    def layers():
        return self.graph['layers']