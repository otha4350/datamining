import requests
import json
import pandas as pd
GET_DATA = False

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
    "ilc_di08": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/ilc_di08/1.0/*.*.*.*.*.*.*?c[freq]=A&c[indic_il]=MED_E&c[unit]=EUR&c[isced11]=ED0-2,ED3_4,ED5-8&c[sex]=T&c[age]=Y18-64&c[geo]=EU,EU27_2020,EU28,EU27_2007,EA,EA20,EA19,EA18,BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,HU,MT,NL,AT,PL,PT,RO,SI,SK,FI,SE,IS,NO,CH,UK,ME,MK,AL,RS,TR,XK&c[TIME_PERIOD]=2024&compress=false&format=json&lang=en",
    #1 value
    "ilc_di18": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/ilc_di18/1.0/*.*.*.*?c[freq]=A&c[statinfo]=MED&c[unit]=INX&c[geo]=EU27_2020,EA20,BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,HU,MT,NL,AT,PL,PT,RO,SI,SK,FI,SE,IS,NO,CH,UK,TR&c[TIME_PERIOD]=2024&compress=false&format=json&lang=en",
    #divided by education level
    "ilc_pw01": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/ilc_pw01/1.0/*.*.*.*.*.*.*.*?c[freq]=A&c[statinfo]=AVG&c[unit]=RTG&c[isced11]=TOTAL,ED0-2,ED3_4,ED5-8&c[life_sat]=LIFE&c[sex]=T&c[age]=Y_GE16&c[geo]=EU27_2020,EA20,BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,HU,MT,NL,AT,PL,PT,RO,SI,SK,FI,SE,IS,NO,CH,UK,ME,MK,AL,RS,TR,XK&c[TIME_PERIOD]=2024&compress=false&format=json&lang=en",
    #1 value
    "ilc_lvho07a": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/ilc_lvho07a/1.0/*.*.*.*.*.*?c[freq]=A&c[unit]=PC&c[incgrp]=TOTAL&c[age]=TOTAL&c[sex]=T&c[geo]=EU,EU27_2020,EU28,EU27_2007,EA,EA20,EA19,EA18,BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,HU,MT,NL,AT,PL,PT,RO,SI,SK,FI,SE,IS,NO,CH,UK,ME,MK,AL,RS,TR,XK&c[TIME_PERIOD]=2024&compress=false&format=json&lang=en",
    #1 value
    "hbs_exp_t111": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/hbs_exp_t111/1.0/*.*.*?c[freq]=A&c[unit]=EUR_AE&c[geo]=EU27_2020,EU28,EU27_2007,EU25,EU15,EA,EA20,EA18,EA17,EA13,EA12,BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,HU,MT,NL,AT,PL,PT,RO,SI,SK,FI,SE,EEA30_2007,EEA28,EFTA,NO,UK,ME,MK,RS,TR,XK&c[TIME_PERIOD]=2020&compress=false&format=json&lang=en",
    # all activities ; Professional, scientific and technical activities
    "lfsa_ewhun2": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/lfsa_ewhun2/1.0/*.*.*.*.*.*.*.*?c[freq]=A&c[nace_r2]=TOTAL,M&c[wstatus]=EMP&c[worktime]=TOTAL&c[age]=Y15-64&c[sex]=T&c[unit]=HR&c[geo]=EU27_2020,EA20,BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,HU,MT,NL,AT,PL,PT,RO,SI,SK,FI,SE,IS,NO,CH,UK,BA,ME,MK,RS,TR&c[TIME_PERIOD]=2024&compress=false&format=json&lang=en",
    # 1 value
    "crim_hom_ocit": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/crim_hom_ocit/1.0/*.*.*?c[freq]=A&c[unit]=NR,P_HTHAB&c[cities]=BE001C,BG001C,CZ001C,DK001C,DE001C,EE001C,EL001C,ES001C,FR001C,HR001C,IT001C,CY001C,LV001C,LT001C,LU001C,HU001C,MT001C,NL001C,AT001C,PL001C,PT001C,RO001C,SI001C,SK001C,FI001C,IS001C,LI002C1,NO001C,CH001C,CH002C,BA001C1,ME001C,MK001C,AL001C,RS001C,TR012C,XK001C&c[TIME_PERIOD]=2023&compress=false&format=json&lang=en",
    # divided by education level and police/legal/political system
    "ilc_pw03b": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/ilc_pw03b/1.0/*.*.*.*.*.*.*.*?c[freq]=A&c[domain]=POLC,LEG,POLIT&c[statinfo]=AVG&c[isced11]=TOTAL,ED0-2,ED3_4,ED5_6&c[sex]=T&c[age]=Y_GE16&c[unit]=RTG&c[geo]=EU27_2020,BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,HU,MT,NL,AT,PL,PT,RO,SI,SK,FI,SE,IS,NO,CH,UK,ME,MK,RS,TR&c[TIME_PERIOD]=2013&compress=false&format=json&lang=en",
    #divided by gross/net and euros/%GDP
    "spr_net_gros": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/spr_net_gros/1.0/*.*.*.*?c[freq]=A&c[spdeps]=TOTAL&c[indic_sp]=GSP_MIO_EUR,NSP_MIO_EUR,GSP_PC_GDP,NSP_PC_GDP&c[geo]=EU27_2020,EU28,EU27_2007,EU15,EA20,EA19,EA18,EA12,BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,HU,MT,NL,AT,PL,PT,RO,SI,SK,FI,SE,EEA_X_LI,EFTA_X_LI,IS,NO,CH,UK,BA,ME,MK,RS,TR&c[TIME_PERIOD]=2022&compress=false&format=json&lang=en",
    #divided by gross/net and by function (Total / Sickness/health care / Disability / Old age  / Family/children / Unemployment / Housing )
    #ska man bara ta total? isåfall bara använda spr_net_gros?
    "spr_net_func": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/spr_net_func/1.0/*.*.*.*.*?c[freq]=A&c[spfunc]=TOTAL,SICK,DIS,OLD,FAM,UNE,HOU&c[spdeps]=SPR&c[indic_sp]=GSP_MIO_EUR,NSP_MIO_EUR&c[geo]=EU27_2020,EU28,EU27_2007,EU15,EA20,EA19,EA18,EA12,BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,HU,MT,NL,AT,PL,PT,RO,SI,SK,FI,SE,EEA_X_LI,EFTA_X_LI,IS,NO,CH,UK,BA,ME,MK,RS,TR&c[TIME_PERIOD]=2022&compress=false&format=json&lang=en",
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


if __name__ == "__main__":
    if GET_DATA:
        dump_data()
    datasets = {dsname: json.load(open(dsname + ".json")) for dsname in dataset_urls.keys()}
    df = fill_df(datasets)
    
    #pca och sånt
    #clustering
    print("########################")   

    print(df)

    print("########################")


    print(df.loc["SE"])