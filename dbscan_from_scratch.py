#nos começaremos tentando criar um algoritmo de clustering somente para duas dimensões

from random import randint
import pandas as pd
import numpy as np

def generate_two_spirals(n_points=1000, noise=0.5):
    theta = np.sqrt(np.random.rand(n_points // 2)) * 2 * np.pi 
    r_a = 2 * theta + np.pi 
    r_b = -2 * theta - np.pi  

    x_a = r_a * np.cos(theta) + np.random.normal(0, noise, n_points // 2)
    y_a = r_a * np.sin(theta) + np.random.normal(0, noise, n_points // 2)

    x_b = r_b * np.cos(theta) + np.random.normal(0, noise, n_points // 2)
    y_b = r_b * np.sin(theta) + np.random.normal(0, noise, n_points // 2)

    X = np.vstack((np.column_stack((x_a, y_a)), np.column_stack((x_b, y_b))))
    y = np.hstack((np.zeros(n_points // 2), np.ones(n_points // 2)))

    return X, y

def generate_ds():
    X, y = generate_two_spirals()

    Xs1 = list(X[y == 0,0])
    Ys1 = list(X[y == 0,1])

    Xs2 = list(X[y == 1,0])
    Ys2 = list(X[y == 1,1])

    for i in range(len(Xs2)):
        Xs1.append(Xs2[i])

    for i in range(len(Ys2)):
        Ys1.append(Ys2[i])

    return Xs1, Ys1

def list_concat(list1:list, list2:list):
    for i in range(len(list2)):
        list1.append(list2[i])

    return list1

def Nneighbors(x:int, y:int, radius:float, x_values:list, y_values:list):
        Nn = 0
        neighbors_xy = []

        for i in range(len(x_values)):
            distance = np.sqrt((x - x_values[i])**2 + (y - y_values[i])**2)
            if distance <= radius and (x_values[i], y_values[i]) != (x,y):
                Nn += 1
                neighbors_xy.append((x_values[i], y_values[i]))

        return Nn, neighbors_xy

class DBSCAN:
    def __init__(self, N, radius):
        self.minNeighbors = N
        self.R = radius
        self.done = False
    
    def neighbor_list(self, nl:list, all_tuples:list, new_cluster:list):
        for point in nl:
            x_list, y_list = zip(*all_tuples) if all_tuples else ([], [])

            Nn, neighbors_xy = Nneighbors(point[0], point[1], self.R, x_list, y_list)
            if Nn >= self.minNeighbors:
                for neighbor in neighbors_xy:
                    if neighbor not in new_cluster:
                        new_cluster.append(neighbor)
                        if neighbor in all_tuples:
                            all_tuples.remove(neighbor)

                new_cluster, all_tuples = self.neighbor_list(neighbors_xy, all_tuples, new_cluster)

        return new_cluster, all_tuples

    def fit(self, x_values:list, y_values:list):
        all_tuples = list(zip(x_values, y_values))
        clusters = []

        while all_tuples:
            new_cluster = []
            ind = randint(0, len(all_tuples) - 1)
            point = all_tuples.pop(ind)

            Nn, neighbors_xy = Nneighbors(point[0], point[1], self.R, x_values, y_values)

            if Nn >= self.minNeighbors:
                new_cluster.append(point)
                for neighbor in neighbors_xy:
                    if neighbor in all_tuples:
                        all_tuples.remove(neighbor)
                        new_cluster.append(neighbor)

                new_cluster, all_tuples = self.neighbor_list(neighbors_xy, all_tuples, new_cluster)

                clusters.append(new_cluster)

        return clusters
    
import matplotlib.pyplot as plt

def main():
        x_ds, y_ds = generate_ds()
        plt.scatter(x_ds, y_ds, alpha=0.6, label='Original Data')
        plt.legend()
        plt.show()

        dbscan_object = DBSCAN(N=10, radius=4)
        clusters = dbscan_object.fit(x_ds, y_ds)

        print(f'num_clusters: {len(clusters)}')

        for cluster_idx, cluster in enumerate(clusters):
            x_list = [point[0] for point in cluster]
            y_list = [point[1] for point in cluster]

            plt.scatter(x_list, y_list, alpha=0.6, label=f'Cluster {cluster_idx + 1}')

        plt.legend()
        plt.title('DBSCAN Clusters')
        plt.show()

        return

if __name__ == "__main__":
    main()
