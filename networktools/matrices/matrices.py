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
            
    def __init__(self, rows_file, header=True, from_events=True, weighted=False): 
        self.filename = rows_file[0]
        self.rows = [row for row in rows_file[1]][header:]
        self.from_events = from_events
        self.weighted = weighted

    def get_matrix_name(self): 
        return '{}_adjacency_matrix.csv'.format(self.filename.lower().split('.csv')[0].replace(' ', '_'))

    def get_events(self): 
        df = pd.DataFrame(self.rows)
        return [[sanitize_string(cell) for cell in df[col_name].tolist() if sanitize_string(cell)]
                for col_name in df]

    def create_graph(self): 
        graph = nx.Graph()

        if self.from_events: 
            edges = []

            for event in self.get_events():
                for i in xrange(len(event)): 
                    for j in xrange(i + 1, len(event)): 
                        edges.append((event[i], event[j]))

            for edge in edges: 
                if graph.has_edge(edge[0], edge[1]): 
                    old_weight = graph[edge[0]][edge[1]]['weight']
                    graph[edge[0]][edge[1]]['weight'] = old_weight + 1
                else: 
                    graph.add_edge(edge[0], edge[1], weight=1) 
        else: 
            if is_pairs_network(self.rows): 
                graph.add_edges_from(self.rows)            
            else: 
                print 'This is not a node pairs file.'
                return None
        return graph

    def build(self): 
        graph = self.create_graph()        
        labels = sorted(graph.nodes())
        if not self.weighted: 
            adjacency_matrix = nx.adjacency_matrix(graph, nodelist=labels).todense().tolist()
        else: 
            adjacency_matrix = nx.attr_matrix(graph, edge_attr='weight', rc_order=labels).tolist()

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
        self.filenameA = fileA[0]
        self.rowsA = [row for row in fileA[1]]

        self.filenameB = fileB[0]
        self.rowsB = [row for row in fileB[1]]

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
        