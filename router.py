import math
import pandas as pd
import sys
import networkx
import matplotlib.pyplot as plt

class Router():
    
    def __init__(self, name, graph):
        self.name = name
        self.connection = graph

    def get_path(self, router_name):
        vertices = self.get_distances()

        print("Start: {}\nEnd: {}\nPath: {}\nCost: {}".format(self.name, router_name, "->".join(vertices[router_name]["shortest_path"]), vertices[router_name]["shortest_distance"]))

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
        self.isBidirectional = True

    def add_edge(self, src, dest, cost):
        if src not in self.graph:
            self.graph[src] = {}
            self.graph[src][dest] = cost

        else:
            self.graph[src][dest] = cost

        if self.isBidirectional:
            if dest not in self.graph:
                self.graph[dest] = {}
                self.graph[dest][src] = cost

            else:
                self.graph[dest][src] = cost
        self.vertices.add(src)
        self.vertices.add(dest)

    def display_graph(self):
        display = networkx.DiGraph()
        for vertex in self.vertices:
            display.add_node(vertex)

        for src in self.graph:
            for dest in self.graph[src]:
                display.add_edge(src, dest, weight=self.graph[src][dest])

        while True:
            pos = networkx.planar_layout(display)
            labels = networkx.get_edge_attributes(display, "weight")
            networkx.draw(display, pos, with_labels=True, node_size=500, node_color="red", arrowsize=15)
            networkx.draw_networkx_edge_labels(display, pos, edge_labels=labels)

            plt.savefig("path_graph1.png")
            plt.show(block=False)
            plt.pause(.1)
            i = input("Push enter to continue")
            plt.clf()
            if not i:
                break

def main():
    graph = Graph()
    #graph.isBidirectional = False

    graph.add_edge("a", "b", 7)
    graph.add_edge("a", "c", 9)
    graph.add_edge("a", "f", 14)
    graph.add_edge("b", "c", 10)
    graph.add_edge("b", "d", 15)
    graph.add_edge("c", "d", 11)
    graph.add_edge("c", "f", 2)
    graph.add_edge("c", "g", 6)
    graph.add_edge("d", "e", 6)
    graph.add_edge("e", "f", 9)

    router = Router("a", graph)
    router.get_path("f")
    router.print_routing_table()
    graph.display_graph()

    router_two = Router("b", graph)
    router.remove_router("c")
    router_two.print_routing_table()
    graph.display_graph()


if __name__ == '__main__':
    main()