import math
import pandas as pd
import sys
import networkx

class Router():
    
    def __init__(self, name, graph):
        self.name = name
        self.connection = graph

    def get_path(self, router_name):
        vertices = self.get_distances()

        print("Start: {}\nEnd: {}\nPath: {}\nCost: {}".format(self.name, router_name, "->".join(vertices[router_name]["previous_vertices"]), vertices[router_name]["shortest_distance"]))

    def print_routing_table(self):
        vertices = self.get_distances()

        table = {"from":[],
                 "to":[],
                 "cost": [],
                 "path":[]}

        for vertex in vertices:
            if vertex != self.name:
                table["from"].append(self.name)
                table["to"].append(vertex)
                if vertices[vertex]["shortest_distance"] == math.inf:
                    table["cost"].append(0)
                    table["path"].append("")
                else:
                    table["cost"].append(int(vertices[vertex]["shortest_distance"]))
                    table["path"].append("->".join(vertices[vertex]["shortest_path"]))

        frame = pd.DataFrame(table)
        print(frame)

    def remove_router(self, to_remove):
        for vertex in self.connection.graph:
            if to_remove in self.connection.graph[vertex]:
                del self.connection.graph[vertex][to_remove]
        if to_remove in self.connection.graph:
            del self.connection.graph[to_remove]
        self.connection.vertices.remove(to_remove)
        self.print_routing_table()

    def get_distances(self):
        #print(self.connection.graph)
        visited = []
        paths = {self.name:{"shortest_distance": 0,
                               "shortest_path": self.name}}

        # find all the paths in the graph
        for vertex in self.connection.vertices:
            if self.name != vertex:
                paths[vertex] = {"shortest_distance": math.inf,
                                    "shortest_path": self.name}

        name_of_shortest = self.name
        next_shortest = 0

        i = 0
        while i <= len(paths):
            for neighbour in self.connection.graph[name_of_shortest]:
                if neighbour in paths and neighbour not in visited:
                    if self.connection.graph[name_of_shortest][neighbour] + next_shortest < paths[neighbour]["shortest_distance"]:
                        paths[neighbour]["shortest_distance"] = self.connection.graph[name_of_shortest][neighbour] + paths[name_of_shortest]["shortest_distance"]
                        paths[neighbour]["shortest_path"] = paths[name_of_shortest]["shortest_path"] + neighbour
            visited.append(name_of_shortest)
            next_shortest = math.inf
            for k, v in paths.items():
                if k not in visited and v["shortest_distance"] < next_shortest and k in self.connection.graph:
                    name_of_shortest = k
                    next_shortest = int(v["shortest_distance"])
            i += 1

        return paths

class Graph():

    def __init__(self):
        self.graph = {}
        self.vertices = set()
        self.display = networkx.Graph()

    def add_neighbour(self, src, dest, cost):
        if src not in self.graph:
            self.graph[src] = {}
            self.graph[src][dest] = cost
            self.display.add_edge(src, dest, weight=cost)
        else:
            self.display.add_edge(src, dest, weight=cost)
            self.graph[src][dest] = cost
        if dest not in self.graph:
            self.display.add_edge(src, dest, weight=cost)
            self.graph[dest] = {}
            self.graph[dest][src] = cost
        else:
            self.display.add_edge(src, dest, weight=cost)
            self.graph[dest][src] = cost
            self.vertices.add(src)
            self.vertices.add(dest)

    def print_graph(self):
        for key in self.graph:
            for node in self.graph[key]:
                print(key, "->", node, "=", self.graph[key][node])
    

def main():
    graph = Graph()
    graph.add_neighbour("a", "b", 7)
    graph.add_neighbour("a", "c", 9)
    graph.add_neighbour("a", "f", 14)
    graph.add_neighbour("b", "c", 10)
    graph.add_neighbour("b", "d", 15)
    graph.add_neighbour("c", "d", 11)
    graph.add_neighbour("c", "f", 2)
    graph.add_neighbour("d", "e", 6)
    graph.add_neighbour("e", "f", 9)
    graph.add_neighbour("c", "g", 6)
    #graph.print_graph()
    router = Router("a", graph)
    router_two = Router("b", graph)
    router_two.print_routing_table()
    router.remove_router("c")
    router_two.print_routing_table()
    # router.get_path("f")
    #router.print_routing_table()
    # router.remove_router("c")

if __name__ == '__main__':
    main()