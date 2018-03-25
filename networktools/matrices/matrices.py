from networktools.files.sanitizer import sanitize_string

try: 
    import networkx as nx
except ImportError: 
    print 'You need to install networkx. Try, sudo pip install networkx'


try: 
    import pandas as pd
except ImportError: 
    print 'You need to install pandas. Try, sudo pip install pandas'


class AdjacencyMatrix: 
    def __init__(self, filename, rows, header=True, from_events=True): 
        self.filename = filename
        self.rows = rows[1:] if header else rows        
        self.from_events = from_events

    def get_matrix_name(self): 
        return '{}_adjacency_matrix.csv'.format(self.filename.lower().split('.csv')[0].replace(' ', '_'))

    def get_events(self): 
        df = pd.DataFrame(self.rows)
        return [[sanitize_string(cell) for cell in df[col_name].tolist()[1:] if sanitize_string(cell)]
                for col_name in df]

    def create_graph(self): 
        graph = nx.Graph()

        if self.from_events: 
            for event in self.get_events(): 
                graph.add_edges_from([(event[i], event[j]) for i in xrange(len(event)) 
                    for j in xrange(i + 1, len(event))])
        else: 
            graph.add_edges_from(self.rows)            
        return graph

    def build(self): 
        graph = self.create_graph()        
        labels = sorted(graph.nodes())
        adjacency_matrix = nx.adjacency_matrix(graph, nodelist=labels).todense().tolist()

        for i in xrange(len(adjacency_matrix)): 
            adjacency_matrix[i].insert(0, labels[i])        

        labels.insert(0, '')
        return self.get_matrix_name(), pd.DataFrame.from_records(adjacency_matrix, columns=labels)
