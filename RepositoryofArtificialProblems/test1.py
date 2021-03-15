import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
from sklearn import datasets, decomposition, preprocessing

#x will have be a 500x15 matrix
#y is just 0s and 1
#not sure how they become those

x, y = datasets.make_blobs(
    
    #number of samples
    n_samples = 500,
    
    #feature count, this really means columns
    n_features = 15,
    
    #i think this means we want to clusters
    centers = 2,
    
    #i think this our range
    center_box = (-4.0, 4.0),
    
    #standard deviation
    cluster_std = 1.75,
    
    #setting the randomness
    random_state = 42
    
    )

#mkaing minmaxsclaer so that they are all between [0,1]
x = preprocessing.MinMaxScaler().fit_transform(x)

#now we are making a PCA, not sure what the n_components
pca = decomposition.PCA(n_components = 3)

#Not sure what it did but it did make a 500, 3 array
pca_result = pca.fit_transform(x)

#Not sure what this stuff is
print(pca.explained_variance_ratio_)

#this puts the stuff into a dataframe
pca_df = pd.DataFrame(data = pca_result, columns = ['pc_1', 'pc_2', 'pc_3'])

#not sure what this does
pca_df = pd.concat([pca_df, pd.DataFrame({"label": y})], axis = 1)

#making the 3d map
ax = Axes3D(plt.figure(figsize = (8,8)))

#this is just making a scatter plot and putting in the values that we want
ax.scatter(xs = pca_df['pc_1'], ys = pca_df['pc_2'], zs = pca_df['pc_3'], c = pca_df['label'], s = 25)

#setting axis
ax.set_xlabel("pc_1")
ax.set_ylabel("pc_2")
ax.set_zlabel("pc_3")
plt.show()





