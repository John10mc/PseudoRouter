import math
import pandas as pd

class Router():
    
    def __init__(self, name, graph):
        self.name = name
        self.connection = graph

    def get_path(self, router_name):
        vertices = self.get_distances()


        print("Start: {}\nEnd: {}\nPath: {}\nCost: {}".format(self.name, router_name, "->".join(vertices[router_name]["previous_vertices"] + router_name), vertices[router_name]["shortest_distance"]))

        #sortedVertices = sorted(vertices.items(), key=lambda item:item[0])

    def print_routing_table(self):
        vertices = self.get_distances()

        table = {"from":[],
                 "to":[],
                 "cost": [],
                 "path":[]}

        for vertex in vertices:
            table["from"].append(self.name)
            table["to"].append(vertex)
            table["cost"].append(vertices[vertex]["shortest_distance"])
            table["path"].append("->".join(vertices[vertex]["previous_vertices"]))

        table = pd.DataFrame(table)
        print(table)

    def get_distances(self):
        visited = []
        vertices = {self.name:{"shortest_distance": 0,
                               "previous_vertices": ""}}

        # find all the vertices in the graph
        for vertex in self.connection.graph:
            for dest in self.connection.graph[vertex]:
                vertices[dest] = {"shortest_distance": math.inf,
                                  "previous_vertices": ""}


        smallestName = self.name
        smallestDist = 0

        i = 0
        while i < len(vertices):
            for vertex in self.connection.graph[smallestName]:
                if vertex in vertices and vertex not in visited:
                    if self.connection.graph[smallestName][vertex] + smallestDist < vertices[vertex]["shortest_distance"]:
                        vertices[vertex]["shortest_distance"] = self.connection.graph[smallestName][vertex] + vertices[smallestName]["shortest_distance"]
                        vertices[vertex]["previous_vertices"] = vertices[smallestName]["previous_vertices"] + smallestName
            visited.append(smallestName)
            smallestDist = math.inf
            for k, v in vertices.items():
                if k not in visited and v["shortest_distance"] < smallestDist and k in self.connection.graph:
                    smallestName = k
                    smallestDist = v["shortest_distance"]
            i += 1

        return vertices

class Graph():

    def __init__(self):
        self.graph = {}

    def add_edge(self, src, dest, cost):
        if src not in self.graph:
            self.graph[src] = {}
            self.graph[src][dest] = cost
        else:
            self.graph[src][dest] = cost

    def print_graph(self):
        for key in self.graph:
            for node in self.graph[key]:
                print(key, "->", node, "=", self.graph[key][node])

        

def main():
    graph = Graph()
    graph.add_edge("a", "b", 7)
    graph.add_edge("a", "c", 9)
    graph.add_edge("a", "f", 14)
    graph.add_edge("b", "c", 10)
    graph.add_edge("b", "d", 15)
    graph.add_edge("c", "d", 11)
    graph.add_edge("c", "f", 2)
    graph.add_edge("d", "e", 6)
    graph.add_edge("e", "f", 9)
    #graph.print_graph()
    router = Router("a", graph)
    router.get_path("f")
    router.print_routing_table()

if __name__ == '__main__':
    main()