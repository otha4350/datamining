from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import seaborn as sns

#task 1
data = pd.read_csv('iris_data.csv', sep=";")
labels=pd.read_csv('iris_labels.csv', sep=";")
# print(data.shape)
# print(data.info())
print(data)
# print(labels.info())
data = pd.merge(data,labels,on="id",how="inner")
data.drop(["examiner"],axis=1,inplace=True)
data = data.sort_values("species")
# grid = sns.pairplot(data,hue="species")
# grid.figure.show()

pivot = data.pivot_table(
    values="sl",
    index="species",
    aggfunc=["mean", "std"]
) 
print(pivot[["mean","std"]])


# task 2
print(data.value_counts("species"))

#task 3

print("TASK 3")
print("TASK 3.1")
data = data[data["sw"]!=-9999]
data = data[data["sl"]!=-9999]

pivot = data.pivot_table(
    values="sl",
    index="species",
    aggfunc=["mean", "std"]
) 
print(pivot[["mean","std"]])

print("TASK 3.2")
data = data[data["sw"]<15]
data = data[data["sl"]<15]

pivot = data.pivot_table(
    values="sl",
    index="species",
    aggfunc=["mean", "std"]
) 
print(pivot[["mean","std"]])

# grid = sns.pairplot(data,hue="species")
# grid.savefig("image.jpg")

print("TASK 4")
print("TASK 4.1")
#task 4.1
numeric_data = data[[i for i in data.columns if data[i].dtypes != 'O' and i != "id"]]
minmax_scaled=MinMaxScaler().fit_transform(numeric_data)

minmax_df = data.copy()
minmax_df[numeric_data.columns] = pd.DataFrame(minmax_scaled, columns=numeric_data.columns)
# print (minmax_df)

pivot = minmax_df.pivot_table(
    values="sl",
    index="species",
    aggfunc=["mean", "std"]
) 
print(pivot[["mean","std"]])

scaled_data = StandardScaler().fit_transform(minmax_scaled)

scaled_df = data.copy()
scaled_df[numeric_data.columns] = pd.DataFrame(scaled_data, columns=numeric_data.columns)

pivot = scaled_df.pivot_table(
    values="sl",
    index="species",
    aggfunc=["mean", "std"]
) 
print(pivot[["mean","std"]])


pca = PCA()
principle_components = pca.fit_transform(scaled_data)

print()
print(principle_components)



df = pd.DataFrame(principle_components)
df.columns = numeric_data.columns

# print(data)
# new_data = data.copy()
# data.merge(df)
# new_data[numeric_data.columns] = df
# print(new_data)

# grid = sns.pairplot(new_data,hue="species")
# grid.figure.show()
print(pca.explained_variance_ratio_)
print("")
print(pd.DataFrame(pca.components_,columns=["SepalL","SepalW","PetalL","PetalW"],index=["PC1","PC2","PC3","PC4"]).abs().mean(axis=0))
print("")

print(pd.DataFrame(pca.components_,columns=["SepalL","SepalW","PetalL","PetalW"],index=["PC1","PC2","PC3","PC4"]).abs())

