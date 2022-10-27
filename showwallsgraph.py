from matplotlib import pyplot as plt
import numpy as np

wallcords = np.array([[111,178],[0,178],[0,0],[174,0],[174,103],[217,142],[1106,142],[1124,105],[1124,0],[1237,0],[1237,103],[1255,142],[2152,142],[2198,103],[2198,0],[2389,0],[2390,177],[2278,177],[2235,218],[2235,1040],[2279,1082],[2389,1082],[2389,1259],[2198,1259],[2197,1156],[2153,1116],[1256,1116],[1237,1155],[1237,1259],[1125,1259],[1125,1155],[1107,1116],[220,1116],[177,1155],[177,1259],[0,1259],[0,1082],[111,1082],[153,1040],[153,218]])
plt.plot(wallcords[:,0],wallcords[:,1]) 
lstr = []
for i in range(len(wallcords)): 
  plt.annotate(str(i),(wallcords[i][0],wallcords[i][1]))

plt.show()