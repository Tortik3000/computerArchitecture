import matplotlib.pyplot as plt
import numpy as np
import subprocess
import os

size = [1, 5, 10, 15, 20, 30, 50, 65, 80, 10 ** 2, 150, 10 ** 3, 10 ** 3 + 10 ** 3 / 2, 10 ** 4, 10 ** 4 + 10 ** 4 / 2]

staticTime_2 = []
staticTime_5 = []
staticTime_8 = []
staticTime_12 = []
staticTime_16 = []

threads = [2, 5, 8, 12]

os.system("g++ -fopenmp -O2 normal.cpp -o test.exe")

for i in range(len(threads)):
    for k in range(len(size)):
        sum0 = 0
        for j in range(3):
            proc = subprocess.Popen(["test.exe", f"{threads[i]}", "input.txt", "output.txt", "0", f"{size[k]}"],
                                    stdout=subprocess.PIPE)
            t = proc.stdout.read().decode("utf-8")
            t = t.split()
            sum0 += float(t[3])
            proc.kill()

        if (i == 0):
            staticTime_2.append(sum0 / 3)
        if (i == 1):
            staticTime_5.append(sum0 / 3)
        if (i == 2):
            staticTime_8.append(sum0 / 3)
        if (i == 3):
            staticTime_12.append(sum0 / 3)

staticTime_2 = np.array(staticTime_2)
staticTime_5 = np.array(staticTime_5)
staticTime_8 = np.array(staticTime_8)
staticTime_12 = np.array(staticTime_12)

fig, ax = plt.subplots()

ax.set_title(label='schedule(static) with size')
ax.set_xlabel("Threads")
ax.set_ylabel('Time(sec)', rotation=90)

ax.set_yticks(ticks=np.arange(0, 20, 1))
ax.grid()

ax.plot(size, staticTime_2, label='static_2', color='steelblue')
ax.plot(size, staticTime_5, label="static_5", color="firebrick")
ax.plot(size, staticTime_8, label="static_8", color="forestgreen")
ax.plot(size, staticTime_12, label="static_12", color="gold")

ax.legend()

plt.semilogx()
plt.show()
