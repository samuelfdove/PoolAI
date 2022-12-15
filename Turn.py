
import numpy as np
from Balls import Balls
from Walls import Walls
from Holes import Holes
from findballpos import findballpos
from matplotlib import pyplot as plt
import cProfile
import timeit
import copy       

class Turn(object):
  def __init__(self,ballpos,holecords=[[110,113],[1181,72],[2262,114],[2240,1134],[1181,1188],[112,1147]],wallcords=[[111,178],[0,178],[0,0],[174,0],[174,103],[217,142],[1106,142],[1124,105],[1124,0],[1237,0],[1237,103],[1255,142],[2152,142],[2198,103],[2198,0],[2389,0],[2390,177],[2278,177],[2235,218],[2235,1040],[2279,1082],[2389,1082],[2389,1259],[2198,1259],[2197,1156],[2153,1116],[1256,1116],[1237,1155],[1237,1259],[1125,1259],[1125,1155],[1107,1116],[220,1116],[177,1155],[177,1259],[0,1259],[0,1082],[111,1082],[153,1040],[153,218]]):
    global br
    br = 57.15 #need to change
    global be
    be = 1

    self.w = Walls(wallcords)
    self.h = Holes(holecords)

    self.ballstate=ballpos

    ##for q-based.  Making it not value based
    self.xvel=0
    self.yvel=0

    self.reward=0
    self.done=False

    self.initialstate = ballpos+[self.xvel]+[self.yvel]
    
 
  def taketurn(self,xvel,yvel):
    b = Balls(self.ballstate)
    b.strikecuexy(xvel,yvel)
    log = True
    reward=0
    if log:
      global outfile
      outfile = open('outputtext.txt','w')
    while b.vel.sum()>0:
      b.newpositions()
      reward+=self.h.intoholes(b)
      reward+=b.findcollisions()
      
      if log:
        b.printpos(outfile)

      self.w.wallcollision(b)

    
    if self.h.canContinue==True and b.canContinue==True:
      done=False
    else:
      done=True
    self.h.canContinue=None

    finalstate = np.array([b.xpos,b.ypos]).transpose()

    return finalstate,reward,done

  def step(self,action):
    if action==1: #increase x
      if self.xvel<=3:
        self.xvel += .1
    elif action==2: #decrease x
      if self.xvel>=-3:
        self.xvel -= .1
    elif action==3: #increase y
      if self.yvel<=3:
        self.yvel += .1
    elif action==4: #decrease y
      if self.yvel>=-3:
        self.yvel -= .1
    elif action==5: #take shot
      self.ballstate,self.reward,self.done = self.taketurn(self.xvel,self.yvel)

    return  self.ballstate+[self.xvel]+[self.yvel], self.reward, self.done

  def reset(self):
    self.ballstate=findballpos()

    ##for q-based.  Making it not value based
    self.xvel=0
    self.yvel=0

    self.reward=0
    self.done=False

    self.initialstate = self.ballstate+[self.xvel]+[self.yvel]
    



#speeds of pool ball: https://billiards.colostate.edu/faq/speed/typical/#:~:text=medium%3A%202%2D4%20mph%20%3D,%3D%2011%2D13%20m%2Fs
#5 m/s for fast shot
#this would need .0057 s intervals


def test():
  testpos = [[300,600],[800,600],[900,625],[-100,-100],[-100,-100],[-100,-100],[-100,-100],[-100,-100],[-100,-100],[-100,-100],[-100,-100],[-100,-100],[-100,-100],[-100,-100],[-100,-100],[-100,-100]]
  testpos = [[1591, 797], [-100, -100], [-100, -100], [1751, 316], [-100, -100], [-100, -100], [1243, 352], [-100, -100], [312, 284], [1634, 653], [1378, 607], [-100, -100], [-100, -100], [1674, 774], [583, 770], [-100, -100]]
  t = Turn(testpos)
  t.taketurn(5,0)
  
  # testpos = [[500,1118],[-100,-100],[-100,-100],[-100,-100],[-100,-100],[-100,-100],[-100,-100],[-100,-100],[-100,-100],[-100,-100],[-100,-100],[-100,-100],[-100,-100],[-100,-100],[-100,-100],[-100,-100]]
  # b = Balls(testpos)
  # b.strikecuexy(0,1)
  # w = Walls([[111,178],[0,178],[0,0],[174,0],[174,103],[217,142],[1106,142],[1124,105],[1124,0],[1237,0],[1237,103],[1255,142],[2152,142],[2198,103],[2198,0],[2389,0],[2390,177],[2278,177],[2235,218],[2235,1040],[2279,1082],[2389,1082],[2389,1259],[2198,1259],[2197,1156],[2153,1116],[1256,1116],[1237,1155],[1237,1259],[1125,1259],[1125,1155],[1107,1116],[220,1116],[177,1155],[177,1259],[0,1259],[0,1082],[111,1082],[153,1040],[153,218]])
  # global br
  # br = 57.15 #need to change
  # global be
  # be = 1
  # for i in range(1000):
  #   w.wallcollision(copy.deepcopy(b))



  


#main()
#test()
#cProfile.run('test()')