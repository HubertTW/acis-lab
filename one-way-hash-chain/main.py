import hashlib
import time

start = time.time()

with open('avengers.mp4', 'rb') as file:
    video = file.read()
    file.close()

print("video size :", len(video), "bytes")
idx = -(len(video) % 1024)
print("the #n block size is", abs(idx))

m1 = hashlib.sha256()
m1.update(video[idx:])
chain = [m1.digest()]

counter = 0
for i in range(0, int((len(video) - abs(idx)) / 1024)):
    # concatenate
    block = video[idx - 1024: idx] + chain[counter]

    # hashing
    m = hashlib.sha256()
    m.update(block)

    chain.append(m.digest())

    counter += 1
    idx -= 1024

end = time.time()

print("the Hn is :")
print(chain[-1].hex())
print("elapsed time is :", end - start, "secs")
