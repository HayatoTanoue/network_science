# coding: utf-8
import networkx as nx
import numpy as np

__all__ = ["no_preferential_attachment", "no_growth_barabasi"]

def no_preferential_attachment(n, m):
    """
    優先的選択がないバラバシアルバートグラフ
    
    network schience chapter5.6 model A

    Parameters
    ----------
    n : int
        number of nodes.
    m : int
        number of add node edge.

    Returns
    -------
    G : networkx graph

    """
    
    G = nx.empty_graph(m) #generate m nodes empty graphe
    
    for i in range(n - m):
        nodes = list(G.nodes())
        new_node = nodes[-1] + 1
        G.add_node(new_node)
        
        selected = np.random.choice(nodes, size=m, replace=False)
        
        G.add_edges_from([(new_node, select) for select in selected])
        
    return G

def no_growth_barabasi(n, step):
    """
    成長のないバラバシアルバートグラフ
    
    network schience chapter5.6 model B

    Parameters
    ----------
    n : int
        number of nodes.
    step : int
        number of steps.

    Returns
    -------
    G : networx graph
    """
    G = nx.empty_graph(n) #generate n nodes empty graphe
    
    def select_by_degree(G):
        """ 次数に比例した選択確率によるノード抽選 """
        degree = [G.degree(i) + 1 for i in range(n)] #次数0 でも抽選されるように+1を行う
        total_degree = sum(degree) 
        weight = [i/total_degree for i in degree]
        selected = np.random.choice(range(n), p=weight)
        
        return selected
    
    s = 0
    while s < step:
        #各ステップで無作為に抽選したノードからエッジを一つ張る
        now = np.random.randint(n)
        
        selected = select_by_degree(G)
        while now == selected:
            selected = select_by_degree(G)
        
        G.add_edge(now, selected)
        
        s += 1
    
    return G