import matplotlib.pyplot as plt
import numpy as np
import subprocess
import os

dynamicThreads = []
dynamicTime = []

staticThread = []
staticTime = []

os.system("g++ -fopenmp -O2 normal.cpp -o test.exe")

for i in range(2, 21):
    staticThread.append(i)
    sum0 = 0
    for j in range(3):
        proc = subprocess.Popen(["test.exe", f"{i}", "input.txt", "output.txt", "0"], stdout=subprocess.PIPE)
        t = proc.stdout.read().decode("utf-8")
        t = t.split()

        sum0 += float(t[3])

    staticTime.append(sum0 / 3)
    proc.kill()

for i in range(2, 21):
    dynamicThreads.append(i)
    sum0 = 0
    for j in range(3):
        proc = subprocess.Popen(["test.exe", f"{i}", "input.txt", "output.txt", "1"], stdout=subprocess.PIPE)
        t = proc.stdout.read().decode("utf-8")
        t = t.split()

        sum0 += float(t[3])

    dynamicTime.append(sum0 / 3)
    proc.kill()

staticThreads = np.array(staticThread)
staticTime = np.array(staticTime)

dynamicThreads = np.array(dynamicThreads)
dynamicTime = np.array(dynamicTime)

fig, ax = plt.subplots()

ax.set_title(label='schedule without size')
ax.set_xlabel("Threads")
ax.set_ylabel('Time(sec)', rotation=90)

ax.set_xticks(ticks=np.arange(2, 21, 2))
ax.set_yticks(ticks=np.arange(0, 50, 5))
ax.grid()

ax.plot(staticThreads, staticTime, label='static', color='steelblue')
ax.plot(dynamicThreads, dynamicTime, label="dynamic", color="firebrick")
ax.legend()

plt.show()
