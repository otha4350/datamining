# A1 Submission

This document contains questions to help you reflect about the operations applied to the data during this assignment. You have to fill it in and submit it on Studium (one sheet per group).

## Group number and group members:
- Vincent Andersson
- Otto Hammar
- Oskar Perers
- Filip Malamas
- Sebastian Åkerhielm



## Task 1: Reading the Data

- **What data type have you assigned to attribute id?**  
Python go brrr!

- **What do you think is the practical consequence of setting this data type?**  
Python already assigned a suitable type so it would make little difference other than making the code more readable.

- **What are the average length of sepals (sl) and their standard deviation?**  

Virginica:  
sl[cm] = -11,92  
std[cm] = 364,98  

Setosa:  
sl[cm] = 4,32  
std[cm] = 2,14  

Versicolor:   
sl[cm] = -1,16  
std[cm] = 258,27  


## Task 2: Database Preprocessing

- **How many instances are there for each class?**  
Virginica - 3000  
Setosa - 3000  
Versicolor - 500


## Task 3: Data Cleaning

- **Why is it important to let the system know which values are missing?**

If we don't we might train on inaccurate data or crash the program because the function we are using does not know how to use undefined values.

- **What are the average length of sepals (sl) and their standard deviation after declaring missing values (3.1)?**  

| species       | ls[cm]    | std[cm]  | 
|:--------------|-----------|----------|
|Iris-setosa    |  1.416255 | 0.189330 |
|Iris-versicolor|  4.320000 | 2.141226 |
|Iris-virginica |  5.505370 | 0.551209 |



- **What are the average length of sepals (sl) and their standard deviation after removing outliers (3.2)?**

| species       | ls[cm]    | std[cm]  | 
|:--------------|-----------|----------|
|Iris-setosa    |  1.416255 | 0.189330 |
|Iris-versicolor|  4.226453 | 0.457974 |
|Iris-virginica |  5.505307 | 0.551364 |

- **Do you think the outliers you have removed were noise (that is, wrong measurements) or unusual but correct observations?**

Most likely wrong measurements as we don't see a petal of 50cm making sense. 

- **Would you first handle missing data and then remove outliers, or the other way round? Why?**

Depending on method. If you are to remove missing data then you can first handle missing data and then remove outliers however if you fill it with dummy data/ average data then you must first remove outliers otherwise you will insert new data based on incorrect data that may be miss entered data.

- **Assume your observations (records) represent people in a social network, and one variable stores their degree centrality. Would you remove outliers in this case? why?**

No, because the people with the most incoming/outgoing relationships are the most prolific users of our network, so we should cater to them (by valuing their data highly). And the least connected users may also be interesting in order to understand all types of people in the network. We might also break the network by removing highly connected people in the network.

## Task 4: Data Transformation

- **What are the average length and standard deviation of sepals after min-max normalization?**

| species       | ls[cm]    | std[cm]  | 
|:--------------|-----------|----------|
|Iris-setosa|      0.437961|  0.326222|
|Iris-versicolor|  0.433546|  0.325913|
|Iris-virginica|   0.441271|  0.324773|

- **What are the average length and standard deviation of sepals after standardization?**

| species       | ls[cm]    | std[cm]  | 
|:--------------|-----------|----------|
|Iris-setosa    | -0.002122  |1.002156|
|Iris-versicolor| -0.015686  |1.001204|
|Iris-virginica |  0.008046  |0.997702|

- **How many components have been selected after 4.3?**  
4 are returned because PCA() is called with no arguments, if you were to call it with PCA(n_components=0.95) you get 2.

- **How much variance is captured by the first two components?**  
0.962603488729185 =~ 96%

- **How is the first component defined as a combination of the original attributes?**

|	|SepalL        |SepalW     |PetalL    |PetalW
|:--|--------------|-----------|----------|------
|PC1|0.519962      |0.297933   |0.573007  |0.559051

- **How many components would have been selected after 4.4 (that is, with an attribute expressed on a larger range)?**
2
- **How many components would have been selected after 4.5 (that is, with a outlier)?**
3

## Task 5: Sampling


|                                 |Simple sampling| Bootstrapping| Stratified(5.3)| Stratified(5.4)|
|:--------------------------------|---------------|--------------|----------------|----------------|
|Number of iris versicolor        | 72            | 87           | 1498           | 50             |
|Number of iris setosa            | 63            | 52           | 1498           | 50             |
|Number of iris virginica         | 15            | 11           | 250            | 50             |
|Are there repeated identifiers?  | no            | yes          | no             | no             |
|Does the number of iris versicolor included in the sample change if you change the local random seed? | yes | yes | no | no |
