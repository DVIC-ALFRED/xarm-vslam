from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
import sklearn.neighbors as nb
import sklearn.cluster as ct

def LoadDF(filename):
    return pd.read_csv("../datasets/maps/" + filename + ".csv", sep=" ")

def Plot(map):
    print("Map size :", len(map), "points")
    x = map['x'].values
    y = map['y'].values
    z = map['z'].values
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, c='r', marker='o')
    plt.show()

def Cluster(map, quiet=False):
    #-> DBSCAN minPts value
    #-? Set at 2*dim = 6
    minPts = 6.0

    #-> DBSCAN epsilon value estimations
    neighbors = nb.NearestNeighbors(n_neighbors = 20)
    neighbors_fit = neighbors.fit(map)
    distances, indices = neighbors_fit.kneighbors(map)
    distances = np.sort(distances, axis=0)
    distances = distances[:,1]
    #-? Ideal epsilon parameter at the crook of the elbow
    # plt.plot(distances)
    # plt.show()
    epsilon = 0.2

    #-> Compute clustering, returns cluster label for each point
    clustering = ct.DBSCAN(eps=epsilon, min_samples=minPts).fit(map)

    #-> Print clustering info
    if not quiet:
        labels = clustering.labels_
        #-> Get nb of clusters
        #-? set(labels) to have labels only once
        #-? Remore -1 from lenght if there is a least one -1
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise_ = list(labels).count(-1)
        print("Map size: %d" % len(labels))
        print("Estimated number of clusters: %d" % n_clusters_)
        print("Estimated number of noise points: %d" % n_noise_)
    
    #-> Convert labels from np.ndarray to pd.DataFrame
    labelsColumn = pd.DataFrame(clustering.labels_, columns=["label"])
    map["labels"] = labelsColumn
    return map