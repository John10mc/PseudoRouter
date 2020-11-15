import math
import pandas as pd
import sys
import networkx
import matplotlib.pyplot as plt

class Router():
    
    def __init__(self, name, graph):
        self.name = name
        self.connection = graph

    # get the distances from this router to all other routers and print the distance and path from this router to the router passed as an arugement
    def get_path(self, router_name):
        vertices = self.get_distances()

        print("Start: {}\nEnd: {}\nPath: {}\nCost: {}".format(self.name, router_name, "->".join(vertices[router_name]["shortest_path"]), vertices[router_name]["shortest_distance"]))

    # print a table of the shortest distance and path from this router to all other routers
    def print_routing_table(self):
        vertices = self.get_distances()

        # formatted table for use in pandas
        table = {"from":[],
                 "to":[],
                 "cost": [],
                 "path":[]}

        # loop through a dictionary containing the distance and path from this router to all others and add it to the table
        for vertex in vertices:

            # dont include the distance and path from this router to itself
            if vertex != self.name:
                table["from"].append(self.name)
                table["to"].append(vertex)

                # if a path to another router cant be calculated set its distance to 0 and its path empty
                if vertices[vertex]["shortest_distance"] == math.inf:
                    table["cost"].append(0)
                    table["path"].append("")

                # else add the distance and path from this router to another to the table
                else:
                    table["cost"].append(int(vertices[vertex]["shortest_distance"]))
                    table["path"].append("->".join(vertices[vertex]["shortest_path"]))

        # output the above table in pandas format
        frame = pd.DataFrame(table)
        print(frame)

    # remove a router from the graph and print the updated graph
    def remove_router(self, to_remove):

        # loop through each of the routers and check if an edge is connected to the one to remove
        # if it is remove it from the graph
        for vertex in self.connection.graph:
            if to_remove in self.connection.graph[vertex]:
                del self.connection.graph[vertex][to_remove]

        # remove the router to_remove and all its edges
        if to_remove in self.connection.graph:
            del self.connection.graph[to_remove]

        # remove the router from vertices which is a list of the routers in the graph
        self.connection.vertices.remove(to_remove)
        self.print_routing_table()

    # method to get the distance and path from this router to all other routers
    def get_distances(self):
        visited = []

        # dict to hold all the distances and paths. This router is set 0 and its path is itself
        paths = {self.name:{"shortest_distance": 0,
                               "shortest_path": self.name}}

        # Add and entry in the dict for each router in the graph
        for vertex in self.connection.vertices:
            if self.name != vertex:
                paths[vertex] = {"shortest_distance": math.inf,
                                    "shortest_path": self.name}

        # name_of_shortest will hold the name of whichever router has the shorest distance from this router for each iteration 
        name_of_shortest = self.name

        # next_shortest will hold the distance of whichever router has the shorest distance from this router for each iteration 
        next_shortest = 0

        # continue untill all paths have been calculated
        i = 0
        while i <= len(paths):

            # from the router with the shortest distance from this router, calculate each of its neighbours distance from this router
            for neighbour in self.connection.graph[name_of_shortest]:

                # check to see if the path being calculated is shorter than the existing path to the neighbour
                if self.connection.graph[name_of_shortest][neighbour] + next_shortest < paths[neighbour]["shortest_distance"]:

                    # if the above is true then update the new distance to that neighbour
                    paths[neighbour]["shortest_distance"] = self.connection.graph[name_of_shortest][neighbour] + paths[name_of_shortest]["shortest_distance"]
                    
                    # the path to that neighbour will be set to the path to current shortest path plus itself
                    paths[neighbour]["shortest_path"] = paths[name_of_shortest]["shortest_path"] + neighbour

            # add name_of_the shortest to visited so that it wont be checked again 
            visited.append(name_of_shortest)

            # reset the next_shortest to infinite so that everything is smaller
            next_shortest = math.inf

            # fine the next shortest distance from this router that hasnt been visited and repeat the process
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

        # allows the graph to be unidirectional or bidirectional
        self.isBidirectional = True

    # add an edge to the graph
    def add_edge(self, src, dest, cost):

        # check to see if src is already a key in the dict
        if src not in self.graph:

            # add the src as a key in the graph dict and let its value be a dict
            self.graph[src] = {}
            # in the src dict add the dest as a key and set its value to the cost passed into the arguement
            self.graph[src][dest] = cost

        # no need to add the src as a key so just add the dest and cost to the src dict
        else:
            self.graph[src][dest] = cost

        # graph will become bidirectional if isBidirectional is True
        if self.isBidirectional:
            # check to see if dest is already a key in the dict
            if dest not in self.graph:
                # add the dest as a key in the graph dict and let its value be a dict
                self.graph[dest] = {}
                # in the dest dict add the dest as a key and set its value to the cost passed into the arguement
                self.graph[dest][src] = cost

            # no need to add the src as a key so just add the dest and cost to the src dict
            else:
                self.graph[dest][src] = cost
        # add the source and destination into vertices to repesent that they are both routers in the graph
        self.vertices.add(src)
        self.vertices.add(dest)

    # method used to display the graph as a graphic
    def display_graph(self):

        # create a directed graph
        display = networkx.DiGraph()

        #loop through all the routers and add them as a node in the directed graph
        for vertex in self.vertices:
            display.add_node(vertex)

        # loop through all the keys(sources) dict in the graph dict and add the src - dest as an edge and the cost as a lable to the directed graph
        for src in self.graph:
            for dest in self.graph[src]:
                display.add_edge(src, dest, weight=self.graph[src][dest])

        # while loop to wait for the user to hit enter to continue
        while True:

            # position the nodes without edge intersections
            pos = networkx.planar_layout(display)

            # lable the edges with the cost from src to dest
            labels = networkx.get_edge_attributes(display, "weight")

            # draw the nodes of the graphs based on the position defined earlier
            networkx.draw(display, pos, with_labels=True, node_size=500, node_color="red", arrowsize=15)

            # draw the edges of the graph based on the position defined earlier
            networkx.draw_networkx_edge_labels(display, pos, edge_labels=labels)

            # display the graph and allow the program to continue
            plt.show(block=False)

            # pause the program execution so that the graphice can be rendered
            plt.pause(.1)
            i = input("Push enter to continue")

            # clear the graphic
            plt.clf()

            # break the loop when input is provided
            if not i:
                break

def main():
    graph = Graph()

    ### Uncomment the line below to enable unidirectional graph ###
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