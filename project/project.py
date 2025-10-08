import requests
import json
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt
import geojson
import plotly.graph_objects as go
from plotly.offline import plot
from plotly.colors import qualitative
import matplotlib.colors as mcolors

GET_DATA = True

def get_request(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            posts = response.json()
            return posts
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

dataset_urls = {
    #divided by education level
    "ilc_di08": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/ilc_di08/1.0/*.*.*.*.*.*.*?c[freq]=A&c[indic_il]=MED_E&c[unit]=PPS&c[isced11]=ED5-8&c[sex]=T&c[age]=Y18-64&c[geo]=EU,EU27_2020,EU28,EU27_2007,EA,EA20,EA19,EA18,BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,HU,MT,NL,AT,PL,PT,RO,SI,SK,FI,SE,IS,NO,CH,UK,ME,MK,AL,RS,TR,XK&c[TIME_PERIOD]=2024&compress=false&format=json&lang=en",
    #1 value
    "ilc_di18": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/ilc_di18/1.0/*.*.*.*?c[freq]=A&c[statinfo]=MED&c[unit]=INX&c[geo]=EU27_2020,EA20,BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,HU,MT,NL,AT,PL,PT,RO,SI,SK,FI,SE,IS,NO,CH,UK,TR&c[TIME_PERIOD]=2024&compress=false&format=json&lang=en",
    #divided by education level
    "ilc_pw01": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/ilc_pw01/1.0/*.*.*.*.*.*.*.*?c[freq]=A&c[statinfo]=AVG&c[unit]=RTG&c[isced11]=ED5-8&c[life_sat]=LIFE&c[sex]=T&c[age]=Y_GE16&c[geo]=EU27_2020,EA20,BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,HU,MT,NL,AT,PL,PT,RO,SI,SK,FI,SE,IS,NO,CH,UK,ME,MK,AL,RS,TR,XK&c[TIME_PERIOD]=2024&compress=false&format=json&lang=en",
    #1 value
    "ilc_lvho07a": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/ilc_lvho07a/1.0/*.*.*.*.*.*?c[freq]=A&c[unit]=PC&c[incgrp]=TOTAL&c[age]=TOTAL&c[sex]=T&c[geo]=EU,EU27_2020,EU28,EU27_2007,EA,EA20,EA19,EA18,BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,HU,MT,NL,AT,PL,PT,RO,SI,SK,FI,SE,IS,NO,CH,UK,ME,MK,AL,RS,TR,XK&c[TIME_PERIOD]=2024&compress=false&format=json&lang=en",
    #1 value
    "hbs_exp_t111": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/hbs_exp_t111/1.0/*.*.*?c[freq]=A&c[unit]=EUR_AE&c[geo]=EU27_2020,EU28,EU27_2007,EU25,EU15,EA,EA20,EA18,EA17,EA13,EA12,BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,HU,MT,NL,AT,PL,PT,RO,SI,SK,FI,SE,EEA30_2007,EEA28,EFTA,NO,UK,ME,MK,RS,TR,XK&c[TIME_PERIOD]=2020&compress=false&format=json&lang=en",
    # all activities ; Professional, scientific and technical activities
    "lfsa_ewhun2": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/lfsa_ewhun2/1.0/*.*.*.*.*.*.*.*?c[freq]=A&c[nace_r2]=M&c[wstatus]=EMP&c[worktime]=TOTAL&c[age]=Y15-64&c[sex]=T&c[unit]=HR&c[geo]=EU27_2020,EA20,BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,HU,MT,NL,AT,PL,PT,RO,SI,SK,FI,SE,IS,NO,CH,UK,BA,ME,MK,RS,TR&c[TIME_PERIOD]=2024&compress=false&format=json&lang=en",
    # 1 value
    "crim_hom_ocit": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/crim_hom_ocit/1.0/*.*.*?c[freq]=A&c[unit]=NR,P_HTHAB&c[cities]=BE001C,BG001C,CZ001C,DK001C,DE001C,EE001C,EL001C,ES001C,FR001C,HR001C,IT001C,CY001C,LV001C,LT001C,LU001C,HU001C,MT001C,NL001C,AT001C,PL001C,PT001C,RO001C,SI001C,SK001C,FI001C,IS001C,LI002C1,NO001C,CH001C,CH002C,BA001C1,ME001C,MK001C,AL001C,RS001C,TR012C,XK001C&c[TIME_PERIOD]=2023&compress=false&format=json&lang=en",
    # divided by education level and police/legal/political system
    # "ilc_pw03b": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/ilc_pw03b/1.0/*.*.*.*.*.*.*.*?c[freq]=A&c[domain]=POLC,LEG,POLIT&c[statinfo]=AVG&c[isced11]=ED5_6&c[sex]=T&c[age]=Y_GE16&c[unit]=RTG&c[geo]=EU27_2020,BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,HU,MT,NL,AT,PL,PT,RO,SI,SK,FI,SE,IS,NO,CH,UK,ME,MK,RS,TR&c[TIME_PERIOD]=2013&compress=false&format=json&lang=en",
    #divided by gross/net and euros/%GDP
    "spr_net_gros": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/spr_net_gros/1.0/*.*.*.*?c[freq]=A&c[spdeps]=TOTAL&c[indic_sp]=NSP_PC_GDP&c[geo]=EU27_2020,EU28,EU27_2007,EU15,EA20,EA19,EA18,EA12,BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,HU,MT,NL,AT,PL,PT,RO,SI,SK,FI,SE,EEA_X_LI,EFTA_X_LI,IS,NO,CH,UK,BA,ME,MK,RS,TR&c[TIME_PERIOD]=2022&compress=false&format=json&lang=en",
    #divided by gross/net and by function (Total / Sickness/health care / Disability / Old age  / Family/children / Unemployment / Housing )
    "spr_net_func": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/spr_net_func/1.0/*.*.*.*.*?c[freq]=A&c[spfunc]=TOTAL,SICK,DIS,OLD,FAM,UNE,HOU&c[spdeps]=SPR&c[indic_sp]=NSP_PC_GDP&c[geo]=EU27_2020,EU28,EU27_2007,EU15,EA20,EA19,EA18,EA12,BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,HU,MT,NL,AT,PL,PT,RO,SI,SK,FI,SE,EEA_X_LI,EFTA_X_LI,IS,NO,CH,UK,BA,ME,MK,RS,TR&c[TIME_PERIOD]=2022&compress=false&format=json&lang=en",
}
def dump_data():
    for dsname, dsurl in dataset_urls.items():
        data = get_request(dsurl)
        with open(f"{dsname}.json", "w") as f:
            json.dump(data, f)

def handle_one_dataset(dataset, dataset_name):
    dim_sizes = dataset["size"]
    dim_ids = dataset["id"]
    dims = [(s, id) for s,id in zip(dim_sizes, dim_ids) if s > 1 and id!="geo" and id!="cities"]

    dim_names = [(dataset_name, 0)]
    for dim_number, dim_id in dims:
        new_dim_names = []
        for dim_name, dim_index in dim_names:
            for key_name,key_index in dataset["dimension"][dim_id]["category"]["index"].items():
                new_dim_names.append((dim_name+"_"+key_name, dim_index * dim_number + key_index))
        dim_names = new_dim_names

    df = pd.DataFrame(columns=list([name for name, _ in dim_names]))
    if "geo" in dataset["dimension"]:
        index = dataset["dimension"]["geo"]["category"]["index"]
    else:
        index = dataset["dimension"]["cities"]["category"]["index"]
        index = {city[:2]:v for city,v in index.items()}


    values = dataset["value"]
    for dim_name, dim_index in dim_names:
        for country, i in index.items():
            i_shifted = i * dim_index
            val = values[str(i_shifted)] if str(i_shifted) in values.keys() else None
            df.loc[country, dim_name] = val

    return df

def fill_df(datasets):
    datasets = [handle_one_dataset(data, name) for name, data in datasets.items()]
    df = pd.concat(datasets, axis="columns")
    return df

def preprocess_data(df: pd.DataFrame):
    df = df.drop(['EU', 'EU27_2020', 'EU28', 'EU27_2007', 'EA', 'EA20', 'EA19', 'EA18', 'EU25', 'EU15', 'EA17', 'EA13', 'EA12', 'EEA30_2007', 'EEA28',
       'EFTA','EEA_X_LI', 'EFTA_X_LI'])

    # print(df.isna().sum(axis=1))
    df = df.dropna(axis=1, thresh=int(0.5*len(df.index)))
    df = df.dropna(axis=0, thresh=int(0.5*len(df.columns)))
    # print(df.isna().sum(axis=0))
    df = df.infer_objects(copy=True)
    df = df.fillna(df.mean())
    df = df.dropna(axis=1)
    # print(df.isna().sum(axis=1))

    minmax_scaled=MinMaxScaler(copy=True).set_output(transform="pandas").fit_transform(df)
    scaled = StandardScaler().set_output(transform="pandas").fit_transform(minmax_scaled)
    pca = PCA(n_components=0.95)
    pcaed_data = pca.set_output(transform="pandas").fit_transform(scaled)

    # for i in range(1,len(pca.explained_variance_ratio_)):
    #     print(f"explained variance ratio pca={i}:", sum(pca.explained_variance_ratio_[:i]))
    # scree plot
    # plt.plot(range(len(pca.explained_variance_ratio_)),pca.explained_variance_)
    # plt.show()
    # print(pca.components_)
    return pcaed_data

def cluster(d: pd.DataFrame):
    def plot_dendrogram(model, **kwargs):
        # Create linkage matrix and then plot the dendrogram

        # create the counts of samples under each node
        counts = np.zeros(model.children_.shape[0])
        n_samples = len(model.labels_)
        for i, merge in enumerate(model.children_):
            current_count = 0
            for child_idx in merge:
                if child_idx < n_samples:
                    current_count += 1  # leaf node
                else:
                    current_count += counts[child_idx - n_samples]
            counts[i] = current_count

        linkage_matrix = np.column_stack(
            [model.children_, model.distances_, counts]
        ).astype(float)

        # Plot the corresponding dendrogram
        dendrogram(linkage_matrix, labels=list(d.index), **kwargs)
    
    agg_single = AgglomerativeClustering(n_clusters=None, distance_threshold=5, linkage="complete")
    agg_single.fit(d)

    # plt.title(f"Hierarchical Clustering Dendrogram - {agg_single.get_params()["linkage"]} linkage")
    # # plot the top three levels of the dendrogram
    # plot_dendrogram(agg_single, truncate_mode="level", p=3)
    # plt.xlabel("Number of points in node (or index of point if no parenthesis).")
    # plt.show()
    print(silhouette_score(d,agg_single.labels_))
    return agg_single

def draw_data(d: pd.DataFrame, clustering):
    #snodd från https://stackoverflow.com/a/42915422
    from mpl_toolkits.mplot3d.proj3d import proj_transform
    from matplotlib.text import Annotation

    class Annotation3D(Annotation):
        '''Annotate the point xyz with text s'''

        def __init__(self, s, xyz, *args, **kwargs):
            Annotation.__init__(self,s, xy=(0,0), *args, **kwargs)
            self._verts3d = xyz        

        def draw(self, renderer):
            xs3d, ys3d, zs3d = self._verts3d
            xs, ys, zs = proj_transform(xs3d, ys3d, zs3d, self.axes.M)
            self.xy=(xs,ys)
            Annotation.draw(self, renderer)


    def annotate3D(ax, s, *args, **kwargs):
        '''add anotation text s to to Axes3d ax'''

        tag = Annotation3D(s, *args, **kwargs)
        ax.add_artist(tag)

    # create figure        
    fig = plt.figure(dpi=60)
    ax = fig.add_subplot(projection='3d')

    # plot vertices
    ax.scatter(d["pca0"],d["pca1"],d["pca2"], marker='o',c=clustering.labels_, s = 64)

    xyzn = zip(d["pca0"],d["pca1"],d["pca2"])

    # add vertices annotation.
    for j, xyz_ in enumerate(xyzn): 
        annotate3D(ax, s=str(list(d.index)[j]), xyz=xyz_, fontsize=10, xytext=(-3,3),
                textcoords='offset points', ha='right',va='bottom')    
    
    plt.show()

def draw_map(d, clustering):
    with open("europe.geojson", "r", encoding="utf-8") as f:
        geometry = geojson.load(f)

    # Create a Series mapping country codes to cluster labels
    cluster_labels = pd.Series(clustering.labels_, index=d.index)

    fig = go.Figure([
        go.Choropleth(
            geojson=geometry,
            locations=list(cluster_labels.index),
            z=list(map(str, cluster_labels.values)),
            featureidkey="properties.ISO2",
            autocolorscale=False,
            colorscale=[[i/len(["#FFFFFF", "#FF0000", "#00FF00", "#0000FF"]), c] for i,c in enumerate(["#FFFFFF", "#FF0000", "#00FF00", "#0000FF"])],
            showscale=True  # Remove color bar
        )
    ])

    fig.update_geos(
        fitbounds="locations",
        resolution=50,
        visible=False,
        showframe=False,
        projection={"type": "mercator"},
    )

    plot(fig)
    

if __name__ == "__main__":
    if GET_DATA:
        dump_data()
    datasets = {dsname: json.load(open(dsname + ".json")) for dsname in dataset_urls.keys()}
    df = fill_df(datasets)
    
    #pca och sånt
    # print(df.loc[["SE","XK", "AL", "BA", "PL"]].transpose())
    df = preprocess_data(df)
    
    #clustering
    clustering = cluster(df)

    # davis-balding index /silhouette score
    # check influence of each dataset
    # does the clusters make sense

    draw_data(df, clustering)
    # print(df.index)
    # draw_map(df, clustering)