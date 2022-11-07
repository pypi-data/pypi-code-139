from os import environ

environ["QT_DEVICE_PIXEL_RATIO"] = "0"
environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
environ["QT_SCREEN_SCALE_FACTORS"] = "1"
environ["QT_SCALE_FACTOR"] = "1"


#******************Graph*************************
class Graph:
    # Souce nodes of graph
    nodal1 = []

    #Destination nodes of graph
    nodal2 = []

    # Different representations of a graph
    list_of_edges = []

    def __init__(self, directed=True):
        self.directed = directed
    
    # Add edge to a graph
    def add_edge(self, node1, node2, weight=1):
        self.nodal1.append(node1)
        self.nodal2.append(node2)

        # Add the edge from node1 to node2
        self.list_of_edges.append([node1, node2, weight])
        
        # If a graph is undirected, add the same edge,
        # but also in the opposite direction
        if not self.directed:
            self.list_of_edges.append([node2, node1, weight])

	# Print a graph representation
    def print_edge_list(self):
        num_of_edges = len(self.list_of_edges)

        print("Graph:")
        for i in range(num_of_edges):
            print("edge ", i+1, ": ", self.list_of_edges[i])



#*******************Graph Plotting******************************
import matplotlib.pyplot as plt

class GraphPlot(Graph):
    def plotGraph(self):
        num1 = self.nodal1
        num2 = self.nodal2

        num1.sort()
        num2.sort()

        n = len(self.list_of_edges)
        
        if(num1 == num2):
            e = n/2
            f = n//2

            if(e == f):
                l = f
                
            else:
                l = int(e) + 1

            x = 1
            y = 0
            node1 = []
            node2 = []
            x_values = []
            y_values = []

            for i in range(0, l):
                point1 = [x, 10]
                node1.append(point1)
                if(x>y):
                    y = x
                x += 4

            for i in range(l, n):
                point2 = [y, 1]
                node2.append(point2)
                y -= 4
            node2.append([1,10])

            f_node = node1 + node2
            
            for i in range(0, n+1):
                x_values.append(f_node[i][0])
                y_values.append(f_node[i][1])
            
            text = []
            for i in range(65, 65+n):
                text.append(chr(i))

            for i in range(0,len(x_values)-1):
                if(y_values[i]==10):
                    plt.text(x_values[i], y_values[i]-1, text[i], fontsize = 20)
                else:
                    plt.text(x_values[i], y_values[i]+1, text[i], fontsize = 20)

            plt.plot(x_values, y_values, marker='o', markersize=20, markeredgecolor="red", markerfacecolor="green", linestyle="dashed", linewidth=2)
            plt.show()
        
        else:
            print("\nUnable to draw the graph due to some issues.\n")



#*******************Adjacency List****************************
class Adj_list:
    def __init__(self, directed=True):
        self.directed = directed

        # Initialize the adjacency list
        # Create a dictionary
        self.adj_list = {}

    def add_edge_adj_list(self, node1, node2):
        try:
            if node1 in self.adj_list:
                self.adj_list[node1].append(node2)
                
                if not self.directed:
                    if node2 in self.adj_list:
                        self.adj_list[node2].append(node1)
                    else:
                        self.adj_list[node2] = [node1]
            else:
                self.adj_list[node1] = [node2]
                
                if not self.directed:
                    if node2 in self.adj_list:
                        self.adj_list[node2].append(node1)
                    else:
                        self.adj_list[node2] = [node1]
                
        except IndexError:
            pass
            
    def print_adj_list(self):
        print("Adjaceny List:")
        for i in self.adj_list:
            print(i, ":", self.adj_list[i])



#*******************Adjacency Matrix****************************
class Adj_matrix:
    def __init__(self, num_of_nodes, directed=True):
        self.num_of_nodes = num_of_nodes
        self.directed = directed

        # Initialize the adjacency matrix
        # Create a matrix with `num_of_nodes` rows and columns
        self.adj_matrix = [[0 for column in range(num_of_nodes)] 
                            for row in range(num_of_nodes)]

    def add_edge_adj_matrix(self, node1, node2, weight=1):
        try:
            self.adj_matrix[node1][node2] = weight

            if not self.directed:
                self.adj_matrix[node2][node1] = weight
        except IndexError:
            pass
            
    def print_adj_matrix(self):
        print("Adjaceny Matrix:")
        for i in range(0,len(self.adj_matrix)):
            print(self.adj_matrix[i])
