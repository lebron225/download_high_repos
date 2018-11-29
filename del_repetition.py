

data = []
dic = {}
with open('./download_list', 'r') as f:

    for line in f.readlines():
        data.append(line[:-1])

for key in data:
    dic[key] = 0

with open('./download_list.txt', 'a') as f:
    for key in data:
        dic[key] += 1
        if dic[key] > 1:
            continue
        f.write(key + '\n')