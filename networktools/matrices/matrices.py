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

import csv


class AdjacencyMatrix: 
    @staticmethod
    def str_edge(edge): 
        return '{} and {}'.format(*edge)

    @staticmethod
    def get_comparison_name(filename1, label1, filename2, label2): 
        filename1 = filename1.lower().replace('.csv', '')
        filename2 = filename2.lower().replace('.csv', '')
        return '{fn1} {lb1} vs {fn2} {lb2} Comparison.csv'.format(fn1=filename1, lb1=label1, fn2=filename2, lb2=label2)

    @staticmethod
    def summarize(columns): 
        return [[columns[j][i] for j in xrange(len(columns))] for i in xrange(len(columns[0]))]

    @staticmethod
    def read_rows_file(f, truncated): 
        f = f.read()
        return [row for row in csv.DictReader(f)][truncated:]
            
    def __init__(self, rows_file, header=True, from_events=True): 
        self.filename = rows_file[0]
        self.rows = [row for row in rows_file[1]][header:] #AdjacencyMatrix.read_rows_file(rows_file[1], header)
        self.from_events = from_events

    def get_matrix_name(self): 
        return '{}_adjacency_matrix.csv'.format(self.filename.lower().split('.csv')[0].replace(' ', '_'))

    def get_events(self): 
        df = pd.DataFrame(self.rows)
        return [[sanitize_string(cell) for cell in df[col_name].tolist() if sanitize_string(cell)]
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

        return AdjacencyMatrix.get_comparison_name(self.filename, label1, matrix.filename, label2), [header] + AdjacencyMatrix.summarize(columns)

    def build(self): 
        graph = self.create_graph()        
        labels = sorted(graph.nodes())
        adjacency_matrix = nx.adjacency_matrix(graph, nodelist=labels).todense().tolist()

        for i in xrange(len(adjacency_matrix)): 
            adjacency_matrix[i].insert(0, labels[i])        

        labels.insert(0, '')
        return self.get_matrix_name(), pd.DataFrame.from_records(adjacency_matrix, columns=labels)


class NetworkComparison:
    @staticmethod
    def to_network(rows): 
        nodes = map(sanitize_string, rows[0][1:])
        values = map(lambda x: x[1:], rows[1:]) 

        network = nx.Graph()

        network.add_edges_from([(nodes[i], nodes[j], {'stance': values[i][j]}) 
            for i in xrange(len(nodes)) for j in xrange(i + 1, len(nodes)) if int(values[i][j]) > 0])
        return network

    @staticmethod
    def get_overlap(a, b): 
        return set(a).intersection(set(b))

    @staticmethod
    def get_difference(a, b): 
        return set(a) - set(b)

    @staticmethod
    def summarize(columns): 
        return [[columns[j][i] for j in xrange(len(columns))] for i in xrange(len(columns[0]))]

    def __init__(self, fileA, fileB, labelA, labelB): 
        self.filenameA, self.rowsA = fileA
        self.filenameB, self.rowsB = fileB

        self.labelA, self.labelB = labelA, labelB

    def get_comparison_name(self): 
        networkA_label = self.filenameA.lower().replace('.csv', '').title()
        networkB_label = self.filenameB.lower().replace('.csv', '').title()
        return '{} vs {} Comparison.csv'.format(networkA_label, networkB_label)

    def compare(self): 
        header = [
            'Node Overlap', 'Edge Overlap',
            'Unique Nodes for {}'.format(self.labelA), 'Unique Nodes for {}'.format(self.labelB), 
            'Unique Edges for {}'.format(self.labelA), 'Unique Edges for {}'.format(self.labelB)
        ]

        networkA = NetworkComparison.to_network(self.rowsA)
        networkB = NetworkComparison.to_network(self.rowsB)

        nodesA, edgesA = networkA.nodes(), networkA.edges()
        nodesB, edgesB = networkB.nodes(), networkB.edges()

        columns = add_padding(
            [
                NetworkComparison.get_overlap(nodesA, nodesB), 
                map(AdjacencyMatrix.str_edge, NetworkComparison.get_overlap(edgesA, edgesB)),
                NetworkComparison.get_difference(nodesA, nodesB),
                NetworkComparison.get_difference(nodesB, nodesA),
                map(AdjacencyMatrix.str_edge, NetworkComparison.get_difference(edgesA, edgesB)),
                map(AdjacencyMatrix.str_edge, NetworkComparison.get_difference(edgesB, edgesA)),
            ]
        )
        return self.get_comparison_name(), [header] + NetworkComparison.summarize(columns)