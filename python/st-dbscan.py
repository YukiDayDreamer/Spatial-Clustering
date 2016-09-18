import itertools
import math
import numpy as np
import pprint
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt



# initialize data: 0:x; 1:y; 2:time; 3:label

# data preparation

### random dataset
##n = 150  # num of points
##high = 10  # range of random numbers
##X = [[0 for j in xrange(4)] for i in xrange(n)]
##for i in range(n):
##    for j in range(3):
##        X[i][j] = np.random.rand() * high

# fixed dataset
X = [
      [2, 2, 1, 0], [3, 3, 2, 0], [4, 3, 1, 0], [2, 3, 2, 0],[1, 1, 1, 0],
      [32, 32, 31, 0], [33, 34, 32, 0], [34, 35, 34, 0], [32, 31, 32, 0],[31, 31, 31, 0],
      [100, 100, 10, 0], [103, 102, 11, 0], [100, 101, 9, 0], [102, 102, 12, 0], [101, 103, 10, 0],
      [200, 200, 10, 0], [201, 202, 12, 0], [201, 203, 14, 0], [204, 201, 13, 0], [203, 202, 12, 0],
      [300, 302, 51, 0],
      [400, 402, 101, 0]
     ]


# paras
eps1 = 4   # spatial distance threshold
eps2 = 2    # temporal distance threshold
minPts = 4  # minimum number of points within eps1 and eps2


# spatial distance
def sp_dist(a, b):
    return math.sqrt(math.pow((a[0] - b[0]), 2) + math.pow((a[1] - b[1]), 2))


# temporal distance
def tp_dist(a, b):
    return abs(a[2] - b[2])


# retrieve number of neighbors
def retrieve_neighbors(point, cluster):
    _num_neighbors = 0  # number of neighbor
    _neighbors = []  # list of neighbor
    for _iter in range(len(cluster)):
        _dist1 = sp_dist(point, cluster[_iter])
        _dist2 = tp_dist(point, cluster[_iter])
        if _dist1 <= eps1 and _dist2 <= eps2:
            _num_neighbors += 1
            _neighbors.append(_iter)
    return _num_neighbors, _neighbors


# main
def main():
    cluster_label = 0  # label meaning: 0:unmarked; 1,2,3,...:cluster label; "noise":noise
    clusters = []  # final output

    # clustering data points
    for i in range(len(X)):
        num_neighbors, list_neighbors = retrieve_neighbors(X[i], X)

        if num_neighbors < minPts:
            # if it is unmarked, mark it "noise"
            if X[i][3] == 0:
                X[i][3] = "noise"
        else:
            cluster_label += 1  # construct a new cluster
            true_nums = 0  # true num of points in cluster
            cluster = []  # construct cluster

            # mark label for all unmarked neighbors
            for j1 in list_neighbors:
                if X[j1][3] == 0 or X[j1][3] == "noise":  # if no other labels
                    X[j1][3] = cluster_label
                    true_nums += 1
                    cluster.append(X[j1])

            # check the sub-circle of all objects
            while len(list_neighbors) != 0:
                j2 = list_neighbors.pop()
                num_sub_neighbors, list_sub_neighbors = retrieve_neighbors(X[j2], X)

                if num_sub_neighbors >= minPts:
                    for k in list_sub_neighbors:
                        # mark all unmarked neighbors
                        if X[k][3] == 0 or X[k][3] == "noise":  # if no other labels
                            # might include |cluster_avg() - X[index]| < delta_eps                            list_neighbors.append(k)
                            X[k][3] = cluster_label
                            true_nums += 1
                            cluster.append(X[k])

            # remove cluster of small size
            if true_nums < minPts:
                for Y in X:
                    if Y[3] == cluster_label:
                        Y[3] = "noise"
                    else:
                        pass
            else:
                clusters.append(cluster)

    # print cluster status
    print(str(len(clusters)) + " clusters in the data set. \n")
    pprint.pprint(clusters)

    # construct clusters

    # plot 3D scatter for clusters
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    colors = itertools.cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k'])
    for cluster in clusters:
        xs = []
        ys = []
        zs = []
        for item in cluster:
            xs.append(item[0])
            ys.append(item[1])
            zs.append(item[2])
        ax.scatter(xs, ys, zs, c=colors.next(), s=50, marker='o')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    # plot 3D scatter for noise
    # xs = []
    # ys = []
    # zs = []
    # for item in X:
    #     if item[3] == "noise":
    #         xs.append(item[0])
    #         ys.append(item[1])
    #         zs.append(item[2])
    # ax.scatter(xs, ys, zs, c=colors.next(), s=50, marker='o')

    plt.show()

if __name__ == '__main__':
    main()
