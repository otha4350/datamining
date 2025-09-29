# Assignment IV — Submission Sheet

This document contains questions to help you reflect about the operations applied to the data during this assignment. You have to fill it in and submit it on Studium.

---

## Task 0: Warm-up

- **Number of instances:**
???
- **Number of attributes:**
???

**Number of instances in each class:**

| Class | Instances |
|------ | --------- |
| A     |           |
| N     |           |

---

## Task 1: KNN-Based Anomaly Detection

**Performance Results:**
| Metric            | Value |
| ----------------- | ----- |
| AUC-ROC           |       |
| Average Precision |       |

**Visualization Results:**
(Please paste the images you have retrieved in Task 1)

---

## Task 2: Parameter Sensitivity
**Which “n_neighbors” and “method” corresponds to the best performance? Write the number of neighbors and the performance score for the specified metric:**

| Metric (Best)     | n_neighbors | Method | Score |
|-------------------|-------------|--------|-------|
| AUC-ROC           | 8           | mean   | 0.94  |
| Average Precision | 6           | mean   | 0.81  |

---

## Task 3: Local Outlier Factor (LOF)
**Which n_neighbors corresponds to the best performance? Write the number of neighbors and the performance score for the specified metric:**

| Metric (Best)     | n_neighbors | Score |
|-------------------|-------------|-------|
| AUC-ROC           | 4           | 0.52  |
| Average Precision | 4           | 0.26  |

**According to the results from trying different `n_neighbors`, which algorithm (KNN or LOF) is more sensitive to hyperparameters? Please explain your findings below.**

LOF is worse for this dataset BUT is way less sensitive to hyperparameters as the ROC-AUC and Average Precision vary way less as we adjust the hyperparameter

---

## Task 4: Real-world Anomaly Detection

- **Which algorithms and metrics have you chosen for this task? Report and explain the results from your analysis.**
???

- **Have you noticed any difference between the metrics in use and the chosen algorithm?**
???

- **Which algorithm seems more appropriate for this task?**  
???

---

## Task 5 (Optional): Improving Detection Performance

- **Which strategies have you tried for improving the performance? Did they work? If not, can you explain why?**  
???

