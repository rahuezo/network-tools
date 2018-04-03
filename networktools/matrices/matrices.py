from networktools.files.sanitizer import sanitize_string
from validation import is_pairs_network
from formatting import add_padding

try: 
    import networkx as nx
except ImportError: 
    print 'You need to install networkx. Try, sudo pip install networkx'


try: 
    import pandas as pd
except ImportError: 
    print 'You need to install pandas. Try, sudo pip install pandas'


class AdjacencyMatrix: 
    @staticmethod
    def str_edge(edge): 
        return '{} and {}'.format(*edge)

    @staticmethod
    def summarize(columns): 
        return [[columns[j][i] for j in xrange(len(columns))] for i in xrange(len(columns[0]))]

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
            if is_pairs_network(self.rows): 
                graph.add_edges_from(self.rows)            
            else: 
                print 'This is not a node pairs file.'
                return None
        return graph

    def get_overlap(self, a, b): 
        return set(a).intersection(set(b))

    def get_unique(self, a, b): 
        return set(a) - set(b)

    def compare(self, label1, label2, matrix):
        header = [
            'Node Overlap', 
            'Edge Overlap',
            'Unique Nodes for {}'.format(label1),
            'Unique Nodes for {}'.format(label2), 
            'Unique Edges for {}'.format(label1),
            'Unique Edges for {}'.format(label2)
        ] 

        graph_a = self.create_graph()
        graph_b = matrix.create_graph()

        nodes_a, edges_a = graph_a.nodes(), graph_a.edges()
        nodes_b, edges_b = graph_b.nodes(), graph_b.edges()

        columns = add_padding([self.get_overlap(nodes_a, nodes_b), 
            map(AdjacencyMatrix.str_edge, self.get_overlap(edges_a, edges_b)),
            self.get_unique(nodes_a, nodes_b), 
            self.get_unique(nodes_b, nodes_a), 
            map(AdjacencyMatrix.str_edge, self.get_unique(edges_a, edges_b)), 
            map(AdjacencyMatrix.str_edge, self.get_unique(edges_b, edges_a))]
        )

        return [header] + AdjacencyMatrix.summarize(columns)

    def build(self): 
        graph = self.create_graph()        
        labels = sorted(graph.nodes())
        adjacency_matrix = nx.adjacency_matrix(graph, nodelist=labels).todense().tolist()

        for i in xrange(len(adjacency_matrix)): 
            adjacency_matrix[i].insert(0, labels[i])        

        labels.insert(0, '')
        return self.get_matrix_name(), pd.DataFrame.from_records(adjacency_matrix, columns=labels)
