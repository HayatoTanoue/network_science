# coding: utf-8
import collections

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import seaborn as sns
from scipy.optimize import curve_fit

__all__ = ["degree_distribution", "degree_correlation"]


def _exp_func(x, a, b):
    """冪乗関数"""
    return b * (x**a)


def _exp_fit(val1_quan, val2_quan):
    """
    累乗フィッティングを行う関数

    Parameters
    ----------
    val1_quan : numpy ndarray

    val2_quan : numpy ndarray

    --------------------
    return : numpy ndarray
            冪乗フィッティングの係数bと指数a
    """
    # maxfev：関数の呼び出しの最大数, check_finite：Trueの場合NaNが含まれている場合はValueError発生
    l_popt, l_pcov = curve_fit(_exp_func, val1_quan, val2_quan, maxfev=10000, check_finite=False)
    return _exp_func(val1_quan, *l_popt), l_popt


def exp_plot(array_x, array_y, y_fit, l_popt, save_name=None):
    """
    冪乗プロット, フィッティングの可視化

    Parameters
    ----------
    array_x : numpy ndarray
        x 軸の値

    array_y : numpy ndarray
        y 軸の値

    y_fit : numpy ndarray
        フィッティング結果のy

    l_popt : list
        係数a, b

    save_name : string
        プロットを保存する場合の保存名
    """
    sns.set()
    ax = plt.subplot(1, 1, 1)
    ax.scatter(array_x, array_y, color='lime')  # 散布図
    ax.plot(array_x, y_fit, label='model', color='magenta')  # 近似直線
    # 近似の指数を表示
    plt.text(1.0, 1.0, 'a ={}'.format(l_popt[0]), ha='right', va='top', transform=ax.transAxes)
    # 両軸を対数に
    plt.gca().set_xscale("log")
    plt.gca().set_yscale("log")

    plt.gca().set_ylim(top=1)  # y軸の最大を1に固定

    if save_name:
        plt.savefig(save_name + ".png")

    plt.show()


def degree_distribution(G, plot=False, save_name=None):
    """
    次数分布の冪乗フィッティング
    y = b x x ^ a

    input:
        G : networkx graph

        plot : bool 
            冪乗分布とフィッティング結果のグラフの表示の有無

        save_name : string
            プロットを保存する場合の保存名
    --------------------
    return : float
            l_popt[0] : 冪乗の指数 a
            l_popt[1] : 冪乗の係数 b  
    """
    degree_count = collections.Counter(sorted([d for n, d in G.degree()], reverse=True))
    deg, cnt = zip(*degree_count.items())

    array_k = np.array(deg)
    # 出現回数を割合に変換
    array_cnt = np.array(cnt) / nx.number_of_nodes(G)

    y_fit, l_popt = _exp_fit(array_k, array_cnt)

    print('a : {},   b : {}'.format(l_popt[0], l_popt[1]))  # 求めたパラメータa,bを確認

    # plot
    if plot:
        exp_plot(array_k, array_cnt, y_fit, l_popt, save_name)

    return l_popt[0], l_popt[1]


def degree_correlation(G, plot=False, save_name=None):
    """
    次数相関の冪乗フィッティング
    y = b x x ^ a

    input:
        G : networkx graph

        plot : bool
            冪乗分布とフィッティング結果のグラフの表示の有無

        save_name : string
            プロットを保存する場合の保存名
    --------------------
    return : float
            l_popt[0] : 冪乗の指数 a
            l_popt[1] : 冪乗の係数 b  
    """
    # 次数リスト
    degree = dict(G.degree())

    # 近傍ノードの平均次数
    neighbor_ave_degree = nx.average_neighbor_degree(G)

    # 各次数の出現回数
    degree_count = collections.Counter(sorted(degree.values(), reverse=True))

    # knn(ki) 次数相関
    average_k_nn = []
    for k in degree_count.keys():
        node_nums = [num for num in G.nodes() if degree[num] == k]
        average_k_nn.append((k, np.average([neighbor_ave_degree[i] for i in node_nums])))

    array_k = np.array([k[0] for k in average_k_nn])
    array_k_nn = np.array([k[1] for k in average_k_nn])
    y_fit, l_popt = _exp_fit(array_k, array_k_nn)

    print('a : {},   b : {}'.format(l_popt[0], l_popt[1]))  # 求めたパラメータa,bを確認

    if plot:
        exp_plot(array_k, array_k_nn, y_fit, l_popt, save_name)

    return l_popt[0], l_popt[1]
