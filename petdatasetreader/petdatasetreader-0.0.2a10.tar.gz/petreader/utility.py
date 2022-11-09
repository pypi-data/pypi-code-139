import matplotlib.pyplot as plt
# from pydata.graphs.savegraphs import SaveGraph
import os
from collections import defaultdict
import networkx as nx
from petreader.labels import *

colors = {ACTIVITY:                "skyblue",
          ACTIVITY_DATA:           "yellow",
          ACTOR:                   'red',
          AND_GATEWAY:             'black',
          XOR_GATEWAY:             'black',
          CONDITION_SPECIFICATION: 'black',

          FLOW:                    'green',
          SAME_GATEWAY:            'red',
          USES:                    "yellow",
          ACTOR_PERFORMER:         'orange'}


def ShowGraph(graph: nx.Graph,
              outputfolder='./') -> None:
    """
        Save a graph into .dot and create .png and .pdf images of the graph

        graph is the nx graph
        outputfolder is the folder where results are saved

        each node must have a ['attrs'][LABEL] and a ['attrs'][TYPE] attributes

    """
    name = graph.name
    #  save graph in .dot
    nx.nx_agraph.write_dot(graph, os.path.join(outputfolder, name) + '.dot')

    node_labels = dict()
    node_color_map = list()
    #  node attrs
    for node in graph.nodes:
        node_labels[node] = graph.nodes[node]['attrs'][LABEL]
        node_color_map.append(colors[graph.nodes[node]['attrs'][TYPE]])

    edge_labels = dict()
    edge_color_map = list()
    for edge in graph.edges:
        edge_labels[edge] = graph.edges[edge]['attrs'][TYPE]
        edge_color_map.append(colors[graph.edges[edge]['attrs'][TYPE]])

    pos = nx.nx_agraph.graphviz_layout(graph, prog='dot')

    plt.figure(figsize=(8, 8))
    # draw labels
    nx.draw_networkx_nodes(graph,
                           pos,
                           node_color=node_color_map,
                           node_size=500,  # 23,
                           alpha=0.35,
                           )
    # shifty = 1.50
    # shiftx = 0  # -70.0
    # pos_node_labels = {k: (p[0] + shiftx, p[1] + shifty) for k, p in pos.items()}
    nx.draw_networkx_labels(graph,
                            pos,  # _node_labels,
                            labels=node_labels,
                            horizontalalignment='center',
                            verticalalignment='center',  # 'bottom',
                            font_size=11,
                            font_weight='bold',
                            font_color='black')
    nx.draw_networkx_edges(graph,
                           pos,
                           edge_color=edge_color_map,
                           arrows=True,
                           arrowsize=13,
                           arrowstyle='->',
                           )
    nx.draw_networkx_edge_labels(graph,
                                 pos,
                                 edge_labels=edge_labels,
                                 font_size=8,  # 10,
                                 font_color='black')

    ax = plt.gca()
    ax.margins(0.05)
    plt.axis("off")
    plt.tight_layout()

    plt.show()
    # plt.close('all')


def SaveGraph(graph: nx.Graph,
              outputfolder='./') -> None:
    """
        Save a graph into .dot and create .png and .pdf images of the graph

        graph is the nx graph
        outputfolder is the folder where results are saved

        each node must have a ['attrs'][LABEL] and a ['attrs'][TYPE] attributes

    """
    name = graph.name

    node_labels = dict()
    node_color_map = list()
    #  node attrs
    for node in graph.nodes:
        node_labels[node] = graph.nodes[node]['attrs'][LABEL]
        node_color_map.append(colors[graph.nodes[node]['attrs'][TYPE]])

    edge_labels = dict()
    edge_color_map = list()
    for edge in graph.edges:
        edge_labels[edge] = graph.edges[edge]['attrs'][TYPE]
        edge_color_map.append(colors[graph.edges[edge]['attrs'][TYPE]])

    pos = nx.nx_agraph.graphviz_layout(graph, prog='dot')

    plt.figure(figsize=(24, 24))
    # draw labels
    nx.draw_networkx_nodes(graph,
                           pos,
                           node_color=node_color_map,
                           node_size=150,
                           alpha=0.35,
                           )
    # shifty = 1.50
    # shiftx = 0  # -70.0
    # pos_node_labels = {k: (p[0] + shiftx, p[1] + shifty) for k, p in pos.items()}
    nx.draw_networkx_labels(graph,
                            pos,  # _node_labels,
                            labels=node_labels,
                            horizontalalignment='center',
                            verticalalignment='center',  # 'bottom',
                            font_size=11,
                            font_weight='bold',
                            font_color='black')
    nx.draw_networkx_edges(graph,
                           pos,
                           edge_color=edge_color_map,
                           arrows=True,
                           arrowsize=13,
                           arrowstyle='->',
                           )
    nx.draw_networkx_edge_labels(graph,
                                 pos,
                                 edge_labels=edge_labels,
                                 font_size=8,
                                 font_color='black')

    ax = plt.gca()
    ax.margins(0.05)
    plt.axis("off")
    plt.tight_layout()

    #  save graph in .dot
    nx.nx_agraph.write_dot(graph, os.path.join(outputfolder, name) + '.dot')
    #  save graph image
    plt.savefig(os.path.join(outputfolder, name) + '.png',
                format='png', dpi=1000)
    plt.savefig(os.path.join(outputfolder, name) + '.pdf',
                format='pdf', dpi=1000)
