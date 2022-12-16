import numpy as np
from myfuctions import mynorm

class Holes(object):
  def __init__(self,positions):
    self.canContinue=None
    self.holer = 130
    self.xs = np.zeros(len(positions))
    self.ys = np.zeros(len(positions))
    for i in range(len(positions)):
      self.xs[i] = positions[i][0]
      self.ys[i] = positions[i][1]
  
  def intoholes(self,B):
    #constants, ball radius, ball elasticity
    br = 57.15 #need to change
    be = 1
    
    reward = 0
    for i in range(len(B.xpos)):

      if B.vel[i]==0: #not checking balls of velocity 0 
        continue
      
      #assuming default walls
      if B.xpos[i]>153+br+5 and B.xpos[i]<2235-br-5 and B.ypos[i]>142+br+5 and B.ypos[i]<1116-br-5:
        continue


      for j in range(len(self.xs)):

        #checking if xs and ys are close enough
        if B.xpos[i]-self.xs[j]>br or B.ypos[i]-self.ys[j]>br:
          continue

        d = mynorm(np.array([B.xpos[i]-self.xs[j],B.ypos[i]-self.ys[j]]))
        if d<=br:
          B.xpos[i] = -100
          B.ypos[i] = -100
          B.xvel[i] = 0
          B.yvel[i] = 0
          B.xytovt()

          #points
          if i==0:
            reward-=100
            self.canContinue=False
          elif i>0 and i<8:
            reward+=100
            if self.canContinue==None:
              self.canContinue==True
          elif i>8:
            reward-=5
          elif i==8: #8 ball goes in
            if B.xpos[1:8].sum()==-700:
              reward+=200
              self.canContinue=True
            else:
              reward-=1000
              self.canContinue=False
    return reward