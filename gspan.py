from dfscode import DFSCode, DFSEdge
from graph import Graph
from collections import defaultdict


class GSpan():
    def __init__(self, input_file, min_sup) -> None:
        
        self.min_sup = min_sup
        self.input_file = input_file
        self.frequentSubgraphs = []
    

    def read_graph(self, input_file):
        with open(input_file, 'r') as f:
            graph_db = dict()
            graph = None

            for line in f:
                line = line.strip()

                if line[0] == 't':
                    if graph is not None:
                        # graph_db.append(graph)
                        graph_db[graph.id] = graph
                    graph = Graph(line.split()[2])
                elif line[0] == 'v':
                    _, id, label = line.split()
                    graph.add_vertex(int(id), int(label))
                elif line[0] == 'e':
                    _, frm, to, label = line.split()
                    graph.add_edge(int(frm), int(to), int(label))
            
            if graph is not None:
                graph_db[graph.id] = graph
        
        return graph_db

    def mine(self):
        graph_db = self.read_graph(self.input_file)

        self.gspan(graph_db, graph_db.keys(), DFSCode())
        breakpoint()

    def find_isomers(self, dfs_code: DFSCode, graph: Graph):
        isomers = []

        if dfs_code.size == 0:
            return isomers
        
        for v in graph.vertices.values():
            if v.label == dfs_code.edges[0].v1_label:
                isomers.append({0: v.id})

        for edge in dfs_code.edges:
            new_isomers = []
            for isomer in isomers:
                curr_v = isomer[edge.v1]
                # graph.vertices[curr_v].edges
                for e in graph.vertices[curr_v].edges:

                    # if edge.v1 < edge.v2:
                    #     if e.label == edge.edge_label and graph.vertices[e.to].label == edge.v2_label
                    if e.label == edge.edge_label and graph.vertices[e.to].label == edge.v2_label:
                        # new_isomers.append(isomer)
                        if edge.v1 < edge.v2 and e.to not in isomer.values():
                            new_isomers.append({**isomer, edge.v2: e.to})
                        elif edge.v1 > edge.v2 and e.to in isomer.values() and isomer[edge.v2] == e.to:
                            new_isomers.append({**isomer})
            
            isomers = new_isomers
        

        return isomers


        # for e in dfs_code.edges:
        #     for v in graph.vertices.values():
        #         if v.label == e.v1_label:
    
    def dfs_possible_extensions(self, dfs_code:DFSCode, graph:Graph):
        extensions = {}
        if dfs_code.size == 0:
            for vid, vertex in graph.vertices.items():
                for edge in vertex.edges:
                    vertex_label = vertex.label
                    other_vertex_label = graph.vertices[edge.to].label

                    if vertex_label < other_vertex_label:
                        ee = DFSEdge(0, 1, vertex_label, other_vertex_label, edge.label)
                    else:
                        ee = DFSEdge(0, 1, other_vertex_label, vertex_label, edge.label)

                    tmp = extensions.get(ee, set())
                    tmp.add(graph.id)
                    extensions[ee] = tmp
        else:
            isomers = self.find_isomers(dfs_code, graph)
            rm_node = dfs_code.right_most
            
            for isomer in isomers:
                rm_mapped = isomer[rm_node]
                inverted_map = {v: k for k, v in isomer.items()}

                # backward edge
                for edge in graph.vertices[rm_mapped].edges:
                    # check if there exist edge from rm_mapped to edge.to in the dfscode
                    # check if it falls on rightmost path
                    if edge.to not in inverted_map:
                        continue

                    inv_to = inverted_map[edge.to]
                    if not dfs_code.check_edge(inv_to, rm_node) and dfs_code.check_on_right_most_path(inv_to) and not dfs_code.is_pre_rm(inv_to):
                        ee = DFSEdge(rm_node, inv_to, graph.vertices[rm_mapped].label, graph.vertices[edge.to].label, edge.label)
                        tmp = extensions.get(ee, set())
                        tmp.add(graph.id)
                        extensions[ee] = tmp
                
                # forward edge
                for v in dfs_code.right_most_path:
                    v1_mapped = isomer[v]

                    for edge in graph.vertices[v1_mapped].edges:
                        if edge.to in inverted_map:
                            continue

                        ee = DFSEdge(v, rm_node+1, graph.vertices[v1_mapped].label, graph.vertices[edge.to].label, edge.label)
                        tmp = extensions.get(ee, set())
                        tmp.add(graph.id)
                        extensions[ee] = tmp
        
        return extensions
                




    
    def possible_extensions(self, graph_db, search_gids, dfs_code: DFSCode):
        extensions = {}
        if dfs_code.size == 0:
            for gid in search_gids:
                graph = graph_db[gid]
                for vid, vertex in graph.vertices.items():
                    for edge in vertex.edges:
                        vertex_label = vertex.label
                        other_vertex_label = graph.vertices[edge.to].label

                        if vertex_label < other_vertex_label:
                            ee = DFSEdge(0, 1, vertex_label, other_vertex_label, edge.label)
                        else:
                            ee = DFSEdge(0, 1, other_vertex_label, vertex_label, edge.label)

                        tmp = extensions.get(ee, set())
                        tmp.add(gid)
                        extensions[ee] = tmp
        else:
            for gid in search_gids:
                isomers = self.find_isomers(dfs_code, graph_db[gid])
                # breakpoint()
                rm_node = dfs_code.right_most

                for isomer in isomers:
                    rm_mapped = isomer[rm_node]
                    inverted_map = {v: k for k, v in isomer.items()}

                    # backward edge
                    for edge in graph_db[gid].vertices[rm_mapped].edges:
                        # check if there exist edge from rm_mapped to edge.to in the dfscode
                        # check if it falls on rightmost path
                        if edge.to not in inverted_map:
                            continue

                        inv_to = inverted_map[edge.to]
                        if not dfs_code.check_edge(inv_to, rm_node) and dfs_code.check_on_right_most_path(inv_to) and not dfs_code.is_pre_rm(inv_to):
                            ee = DFSEdge(rm_node, inv_to, graph_db[gid].vertices[rm_mapped].label, graph_db[gid].vertices[edge.to].label, edge.label)
                            tmp = extensions.get(ee, set())
                            tmp.add(gid)
                            extensions[ee] = tmp
                    
                    # forward edge
                    for v in dfs_code.right_most_path:
                        v1_mapped = isomer[v]

                        for edge in graph_db[gid].vertices[v1_mapped].edges:
                            if edge.to in inverted_map:
                                continue

                            ee = DFSEdge(v, rm_node+1, graph_db[gid].vertices[v1_mapped].label, graph_db[gid].vertices[edge.to].label, edge.label)
                            tmp = extensions.get(ee, set())
                            tmp.add(gid)
                            extensions[ee] = tmp
        
        return extensions
        
    
    def is_min(self, dfs_code: DFSCode):
        dfs_graph = dfs_code.to_graph()
        tmp_dfs_code = DFSCode()

        

        for edge in dfs_code.edges:
            ext = self.dfs_possible_extensions(tmp_dfs_code, dfs_graph)
            min_ee = None
            # breakpoint()

            for ee, gids in ext.items():
                if min_ee == None:
                    min_ee = ee
                elif min_ee > ee:
                    min_ee = ee
            
            if min_ee is None or min_ee != edge:
                return False
            
            tmp_dfs_code.add(min_ee)
            
        

        return True
        


    def gspan(self, graph_db, search_gids, dfs_code):
        extensions = self.possible_extensions(graph_db, search_gids, dfs_code)
        # breakpoint()

        for extension, gids in extensions.items():
            if len(gids) < self.min_sup:
                continue

            new_dfs_code = DFSCode()
            new_dfs_code.edges = dfs_code.edges.copy()
            new_dfs_code.size = dfs_code.size
            new_dfs_code.right_most = dfs_code.right_most
            new_dfs_code.right_most_path = dfs_code.right_most_path.copy()

            new_dfs_code.add(extension) # WIP

            if self.is_min(new_dfs_code):
                # breakpoint()
                self.frequentSubgraphs.append(new_dfs_code)
                self.gspan(graph_db, gids, new_dfs_code)




if __name__ == "__main__":
    g = GSpan('active.txt', 2)
    # db = g.read_graph('active.txt')
    # ee1 = DFSEdge(0, 1, 2, 2, 1)
    # ee2 = DFSEdge(1, 2, 2, 7, 1)
    # dfs_code = DFSCode()
    # dfs_code.add(ee1)
    # dfs_code.add(ee2)
    # print(dfs_code.edges)
    # res = g.possible_extensions(db, ['0', '3'], dfs_code)
    # print(res)


    g.mine()
    
    # print(db)
