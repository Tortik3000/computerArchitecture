import matplotlib.pyplot as plt
import numpy as np
import subprocess
import os

dynamicSize = [10, 50, 10 ** 2, 150, 10 ** 3, 10 ** 3 + 10 ** 3 / 2, 10 ** 4, 10 ** 4 + 10 ** 4 / 2,
               10 ** 5 + 10 ** 5 / 2, 10 ** 6 + 10 ** 6 / 2]

dynamicTime_2 = []
dynamicTime_5 = []
dynamicTime_8 = []
dynamicTime_12 = []

threads = [2, 5, 8, 12]

os.system("g++ -fopenmp -O2 normal.cpp -o test.exe")

for i in range(4):
    for k in range(len(dynamicSize)):
        sum0 = 0
        for j in range(3):
            proc = subprocess.Popen(["test.exe", f"{threads[i]}", "input.txt", "output.txt", "1", f"{dynamicSize[k]}"],
                                    stdout=subprocess.PIPE)
            t = proc.stdout.read().decode("utf-8")
            t = t.split()
            sum0 += float(t[3])
            proc.kill()

        if (i == 0):
            dynamicTime_2.append(sum0 / 3)
        if (i == 1):
            dynamicTime_5.append(sum0 / 3)
        if (i == 2):
            dynamicTime_8.append(sum0 / 3)
        if (i == 3):
            dynamicTime_12.append(sum0 / 3)

dynamicTime_2 = np.array(dynamicTime_2)
dynamicTime_5 = np.array(dynamicTime_5)
dynamicTime_8 = np.array(dynamicTime_8)
dynamicTime_12 = np.array(dynamicTime_12)

fig, ax = plt.subplots()

ax.set_title(label='schedule(dynamic) with size')
ax.set_xlabel("Threads")
ax.set_ylabel('Time(sec)', rotation=90)

ax.set_xticks(ticks=np.arange(2, 26, 1))
ax.set_yticks(ticks=np.arange(0, 20, 1))
ax.grid()

ax.plot(dynamicSize, dynamicTime_2, label='dynamic_2', color='steelblue')
ax.plot(dynamicSize, dynamicTime_5, label="dynamic_5", color="firebrick")
ax.plot(dynamicSize, dynamicTime_8, label="dynamic_8", color="forestgreen")
ax.plot(dynamicSize, dynamicTime_12, label="dynamic_12", color="gold")
ax.legend()

plt.semilogx()
plt.show()
