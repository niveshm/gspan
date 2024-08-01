from graph import Edge, Graph, Vertex


class DFSEdge():
    def __init__(self, v1, v2, v1_label, v2_label, edge_label):
        self.v1 = v1
        self.v2 = v2
        self.v1_label = v1_label
        self.v2_label = v2_label
        self.edge_label = edge_label

    def __repr__(self):
        return f'({self.v1}, {self.v2}, {self.v1_label}, {self.edge_label}, {self.v2_label})'
    
    def __eq__(self, other):
        if other is None or not isinstance(other, DFSEdge):
            return False
        a = (self.v1, self.v2, self.v1_label, self.edge_label, self.v2_label)
        b = (other.v1, other.v2, other.v1_label, other.edge_label, other.v2_label)
        return a == b
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def pair_check(self, i1, j1, i2, j2):
        i_forward = i1 < j1
        j_forward = i2 < j2
        if i_forward and j_forward:
            return j1 < j2 or (j1 == j2 and i1 > i2)
        elif not i_forward and not j_forward:
            return (i1 == i2 and j1 < j2) or (i1 < i2)
        elif i_forward:
            return j1 <= i2
        else:
            return i1 < j2
    
    def __lt__(self, other):
        a = (self.v1_label, self.edge_label, self.v2_label)
        b = (other.v1_label, other.edge_label, other.v2_label)
        
        if self.pair_check(self.v1, self.v2, other.v1, other.v2):
            return True

        return a < b
    
    def __hash__(self):
        return hash((self.v1, self.v2, self.v1_label, self.edge_label, self.v2_label))


class DFSCode():
    def __init__(self):
        self.right_most = -1
        self.size = 0
        self.right_most_path = []
        self.edges = []
    
    def add(self, edge: DFSEdge): # WIP
        if self.size == 0:
            self.right_most = edge.v2
            self.right_most_path.extend([edge.v1, edge.v2])
        else:
            v1 = edge.v1
            v2 = edge.v2
            if v1 < v2:
                while len(self.right_most_path) > 0 and self.right_most_path[-1] > v1:
                    self.right_most_path.pop()
                self.right_most_path.append(v2)
                self.right_most = v2
            # while len(self.right_most_path) > 0 and self.right_most_path
            



        self.edges.append(edge)
        self.size += 1
    
    def check_edge(self, v1, v2):
        for e in self.edges:
            if (e.v1 == v1 and e.v2 == v2) or (e.v1 == v2 and e.v2 == v1):
                return True
        
        return False
    
    def check_on_right_most_path(self, v):
        return v in self.right_most_path
    
    def is_pre_rm(self, v):
        return self.right_most_path[-2] == v
    
    def to_graph(self):
        graph = Graph(-1)
        for edge in self.edges:
            if edge.v1 not in graph.vertices:
                graph.add_vertex(edge.v1, edge.v1_label)
            if edge.v2 not in graph.vertices:
                graph.add_vertex(edge.v2, edge.v2_label)
            
            graph.add_edge(edge.v1, edge.v2, edge.edge_label)
        
        return graph