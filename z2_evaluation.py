from sampling_2D_Evaluation import *
import csv

baseline = np.linspace(5, 100, num=20, dtype=int)
results = np.zeros((20, 10), dtype=int)

for i in range(len(baseline)):
    num_vertex = baseline[i]

    for j in range(10):
        top, bottom, time = run_experiment(num_vertex)
        results[i][j] = time
    print(i)

with open("results.csv", "w", newline="") as csvfile:
    datawriter = csv.writer(csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
    row = ["experiment 1", "experiment 2", "experiment 3", "experiment 4", "experiment 5",
           "experiment 6", "experiment 7", "experiment 8", "experiment 9", "experiment 10", "mean"]
    datawriter.writerow(row)
    for i in range(20):
        row = results[i]
        row = np.append(row, np.mean(row))
        datawriter.writerow(row)
