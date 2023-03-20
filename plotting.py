f = open("example.csv","r")
import numpy as np
import matplotlib.pyplot as plt
data = []
for line in f:
    data.append(line[:-1].split(";"))
data = data[1:]
ban = {'time':[],'bid':[],'ask':[],'mid':[],'bbid':[],'bask':[],'bmid':[]}
per = {'time':[],'bid':[],'ask':[],'mid':[],'bbid':[],'bask':[],'bmid':[]}
for line in data:
    if line[2]=="PEARLS":
        per['time'].append(float(line[1]))
        per['mid'].append(float(line[15]))
        per['bid'].append({line[3]:line[4],line[5]:line[6],line[7]:line[8]})
        d = {line[3]: line[4], line[5]: line[6], line[7]: line[8]}
        if '' in d:
            del d['']
        e ={}
        for i in d:
            e.update({float(i):d[i]})
        per['bbid'].append(float(min(e.keys())))
        per['ask'].append({line[9]: line[10], line[11]: line[12], line[13]: line[14]})
        d = {line[9]: line[10], line[11]: line[12], line[13]: line[14]}
        if '' in d:
            del d['']
        e={}
        for i in d:
            e.update({float(i): d[i]})
        per['bask'].append(float(max(e.keys())))
    elif line[2]=="BANANAS":
        ban['time'].append(float(line[1]))
        ban['mid'].append(float(line[15]))
        ban['bid'].append({line[3]: line[4], line[5]: line[6], line[7]: line[8]})
        d = {line[3]: line[4], line[5]: line[6], line[7]: line[8]}
        if '' in d:
            del d['']
        e ={}
        for i in d:
            e.update({float(i):d[i]})
        ban['bbid'].append(float(max(e.keys())))
        ban['ask'].append({line[9]: line[10], line[11]: line[12], line[13]: line[14]})
        d = {line[9]: line[10], line[11]: line[12], line[13]: line[14]}
        if '' in d:
            del d['']
        e ={}
        for i in d:
            e.update({float(i):d[i]})
        ban['bask'].append(float(min(e.keys())))
ban['bmid']=[(ban['bask'][i]+ban['bbid'][i])/2 for i in range(len(ban['bask']))]
#plt.plot(per['time'],per['mid'],label="mid")
#plt.plot([i for i in range(len(per['bbid']))],per['bbid'],label="bid")
#plt.plot([i for i in range(len(per['bbid']))],per['bask'],label="ask")
#plt.legend()
#plt.show()

window_size = 5
i = window_size
ma = [4938 for i in range(window_size)]
while i < len(ban['bmid']) - window_size + 1:
    window_average = round(np.sum(ban['bmid'][i-window_size:i+window_size]) / window_size*0.5, 2)
    ma.append(window_average)
    i += 1

plt.plot([i for i in range(len(ban['bbid']))],ban['bbid'],label="bid")
plt.plot([i for i in range(len(ban['bask']))],ban['bask'],label="ask")
plt.plot([i for i in range(len(ma))],ma,label="mid")
plt.legend()
plt.show()
print((ma))
print(len(ban['bask']))
print(np.mean(per['bask']),np.std(per['mid']))
print(np.mean(ban['mid']),np.std(ban['mid']))