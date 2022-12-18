import numpy as np
import threading

f = open("input.txt", "r")
lines = f.readlines()
N = int(lines[0])

matrix = np.loadtxt(lines[1:N + 1])

vector = np.array([float(x) for x in lines[N + 1].split()])

matrix = np.c_[matrix, vector.T]
print("Input matrix:\n", matrix, "\n")

def A(i, k, m, matrix):
    m[(i, k)] = matrix[k, i] / matrix[i, i]


def B(i, j, k, m, n, matrix):
    n[(i, j, k)] = matrix[i, j] * m


def C(j, k, n, matrix):
    matrix[k, j] = matrix[k, j] - n

m = dict()
n = dict()
for i in range(N-1):
    threads = []
    for k in range(i+1, N):
        threads.append(threading.Thread(target = A, args = (i, k, m, matrix)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    threads = []
    for k in range(i+1, N):
        for j in range(i, N+1):
            threads.append(threading.Thread(target = B, args = (i, j, k, m[i, k], n, matrix)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    threads = []
    for k in range(i + 1, N):
        for j in range(i, N+1):
            threads.append(threading.Thread(target = C, args = (j, k, n[(i, j, k)], matrix)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

print("Matrix after Gaussian elimination:\n",matrix, "\n")

for i in range(N-1, -1, -1):
    matrix[i, N] /= matrix[i, i]
    matrix[i, i] /= matrix[i, i]
    for j in range(i-1, -1, -1):
        matrix[j, N] -= matrix[j, i]* matrix[i, N]
        matrix[j, i] -= matrix[j, i]* matrix[i, i]


print("Solved matrix:\n", matrix, "\n")

output = str()
output+=str(N)+"\n"
output+=np.array2string(matrix[:,:N], max_line_width=1000000000, separator=" ", formatter={'float_kind':lambda x: "%.9f" % x}).replace("[","").replace("]","").replace("  "," ")+"\n"
output+=np.array2string(np.transpose(matrix[:,N]), max_line_width=1000000000, separator=" ", formatter={'float_kind':lambda x: "%.9f" % x}).replace("[","").replace("]","").replace("  "," ")

output = output.split("\n")
for i in range(len(output)):
    output[i] = output[i].lstrip()+"\n"

output_f = open("output.txt", "w")
for line in output:
    output_f.write(line)
output_f.close()