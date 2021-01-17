# coding: utf-8
import networkx as nx
import numpy as np

__all__ = ["add_BA_node", "add_random_node"]


def add_BA_node(G, m):
    """
    BA modelの性質である優先的選択に基づいてエッジを接続するノードを追加する

    詳細は network schience chapter5 参照

    Parameters
    ----------
    G : networkx graph

    m : int
        number of add node edge.

    """
    nodes = list(G.nodes())
    new_node = nodes[-1] + 1
    G.add_node(new_node, kind="barabasi")
    # 優先的選択に倣って接続ノードを決定する
    degree = [G.degree(i) + 1 for i in nodes]
    total_degree = sum(degree)
    weight = [i / total_degree for i in degree]
    selected = np.random.choice(nodes, size=m, p=weight, replace=False)
    # 選択ノードとのエッジを追加
    G.add_edges_from([(new_node, node) for node in list(selected)])


def add_random_node(G, p):
    """
    新しくノードを追加し,追加ノードから既存ノードに対してp(接続確率)の確率でエッジを張る

    Parameters
    ----------
    G : networkx graph

    p : float
        既存ノードへの接続確率 (0 <= p <= 1)

    """
    nodes = list(G.nodes())
    new_node = nodes[-1] + 1
    G.add_node(new_node, kind="random")
    for node in nodes:
        # 乱数によって接続の有無を決定する
        if np.random.random() <= p:
            G.add_edge(new_node, node)
