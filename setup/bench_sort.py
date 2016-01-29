import time
import random

start = time.time()

result = []
for x in range(1000000):
    result.append({"key":x, "score":random.randint(1, 100000)})

print "List building time: ", time.time() - start

result = sorted(result, key=lambda x: x['score'])

print result[0:10]

print "Total time after sorting: ",  time.time() - start
