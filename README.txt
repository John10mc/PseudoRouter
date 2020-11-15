dependencies:
pandas              1.1.4
networkx            2.5
matplotlib          3.3.3

Added features:
Used networkx to create a graphic of the graph where the edges are repesented as arrows indicating their direction and the cost of the edge is shown
Allows the user to set if the graph is bidirectional or unidirectional (set to bidirectional by default)

Note:
Added a new edge from c to g to display how the paths are recalcuated when c is removed
Graphic shows that g has no connection to the network after removal