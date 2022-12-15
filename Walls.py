import numpy as np
from myfuctions import mynorm
import Balls

class Walls(object):
  def __init__(self,positions):
    self.Ps = np.zeros([len(positions),2])
    self.Qs = np.zeros([len(positions),2])
    self.PQvec =np.zeros([len(positions),2])
    self.PQuvec =np.zeros([len(positions),2])
    for i in range(len(positions)):
      ip1 = i+1
      if i==len(positions)-1:
        ip1 = 0
      self.Ps[i] = positions[i]
      self.Qs[i] = positions[ip1]
      self.PQvec[i][0] = positions[ip1][0]-positions[i][0]
      self.PQvec[i][1] = positions[ip1][1]-positions[i][1]
      magnitudes = mynorm(self.PQvec[i])
      self.PQuvec[i] = np.divide(self.PQvec[i],magnitudes)

  def wallcollision(self,Ballz: Balls):
    #constants, ball radius, ball elasticity
    br = 57.15 #need to change
    be = 1

    global outputcols
    #following this: https://www.youtube.com/watch?v=hBWOxNLH4Dw
    # B = np.array([Ballz.xpos,Ballz.ypos]).transpose()
    # V = np.array([Ballz.xvel,Ballz.yvel]).transpose()
    numballs = len(Ballz.xpos)
    numwalls = len(self.Ps)
    


    for i in range(numballs):

      if Ballz.vel[i]==0: #not checking balls of velocity 0 
        continue

      Bx = Ballz.xpos[i]
      By = Ballz.ypos[i]
      V = np.array([Ballz.xvel[i],Ballz.yvel[i]])

      
      #assuming default walls, making sure they are anywhere close to walls
      # if Bx>153+br and Bx<2235-br and By>142+br and By<1116-br:
      #   continue

      #assuming default walls, limiting applicable walls.
      js = []
      if By<500:
        if Bx<500:
          js = [38,39,0,1,2,3,4,5]
        elif Bx >=500 and Bx<=1500:
          js = [5,6,7,8,9,10,11]
        else:
          js = [11,12,13,14,15,16,17,18]
      else:
        if Bx<500:
          js = [31,32,33,34,35,36,37,38]
        elif Bx >=500 and Bx<=1500:
          js = [25,26,27,28,29,30,31]
        else:
          js = [18,19,20,21,22,23,24,25]

      #for j in range(numwalls):
      for j in js:

        B = np.array([Bx,By])

        a = np.dot((self.Ps[j]-B),self.PQuvec[j])
        if a>0: #closest point is start of wall
          C = self.Ps[j]
        elif np.dot(B-self.Qs[j],self.PQuvec[j])>0: #closest point is end of wall
          C = self.Qs[j]
        else: #closest point is middle of wall
          A = self.PQuvec[j]*a
          D = (self.Ps[j]-B)-A
          C = (B+D)
          C =  B + (self.Ps[j]-B)-(self.PQuvec[j]*(np.dot((self.Ps[j]-B),self.PQuvec[j])))
        dis = B-C
        if mynorm(dis) <=br/2 and np.dot(dis,V)<0:

          
          #repositioning ball
          disuvec = dis/mynorm(dis)
          # repositionedB = B+np.multiply(disuvec,br-mynorm(dis))
          # Ballz.xpos[i] = repositionedB[0]
          # Ballz.ypos[i] = repositionedB[1]

          #newvelocity
          #copying video
          sepVel = np.dot(V,disuvec)


          
          newV = V+np.multiply(disuvec,-sepVel*be-sepVel)
          Ballz.xvel[i] = newV[0]
          Ballz.yvel[i] = newV[1]
          Ballz.xytovt()