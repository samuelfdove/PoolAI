import random
import math

def mindis(ballpos,newloc):
  mind = 30000
  for i in range(len(ballpos)):
    d = math.sqrt((ballpos[i][0]-newloc[0])**2+(ballpos[i][1]-newloc[0])**2)
    if d<mind:
      mind=d
  
  return mind


def findballpos():
  ballpos = []
  for i in range(16):
    # if I don't want all balls
    # if i!=0 and i!=8:
    #   if random.random() >=.5:
    #     ballpos.append([-100,-100])
    #     continue

    newloc = [random.randint(183,2205),random.randint(172,1086)]
    if i==0:
      ballpos.append(newloc)
    else:
      while mindis(ballpos,newloc)<=70.15:
        newloc = [random.randint(183,2205),random.randint(172,1086)]
      ballpos.append(newloc)
  return ballpos
  
