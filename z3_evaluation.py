from sampling_3D_Evaluation import *
import csv

baseline = np.linspace(2, 16, num=15, dtype=int)
results = np.zeros((15, 10), dtype=int)

for i in range(len(baseline)):
    num_vertex = baseline[i]

    for j in range(10):
        top, bottom, time = run_experiment(num_vertex)
        results[i][j] = time
    print(baseline[i])

with open("results_3d.csv", "w", newline="") as csvfile:
    datawriter = csv.writer(csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
    row = ["experiment 1", "experiment 2", "experiment 3", "experiment 4", "experiment 5",
           "experiment 6", "experiment 7", "experiment 8", "experiment 9", "experiment 10", "mean", "row number"]
    datawriter.writerow(row)
    for i in range(15):
        row = results[i]
        row = np.append(row, np.mean(row))
        row = np.append(row, baseline[i])
        datawriter.writerow(row)
