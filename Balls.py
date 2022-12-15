import numpy as np
from myfuctions import mynorm

class Balls(object):
  def __init__(self,positions):
    self.canContinue=None
    self.firstCollision=True

    self.xpos = np.zeros([16])
    self.ypos = np.zeros([16])
    self.xvel = np.zeros([16])
    self.yvel = np.zeros([16])
    self.vel = np.zeros([16])
    self.theta = np.zeros([16])
    
    for i in range(len(positions)):
      if positions[i][0]==-100: #positions[i]==None or 
        self.xpos[i] = -100
        self.ypos[i] = -100
      else:
        self.xpos[i] = positions[i][0]
        self.ypos[i] = positions[i][1]
  
  def xytovt(self):
    self.vel = np.sqrt(np.square(self.xvel)+np.square(self.yvel))
    self.theta = np.arctan2(self.yvel,self.xvel)

  def vttoxy(self):
    self.xvel = self.vel*np.cos(self.theta)
    self.yvel = self.vel*np.sin(self.theta)

  def strikecuexy(self,newxvel,newyvel):
    self.xvel[0]=newxvel
    self.yvel[0] =newyvel
    self.xytovt()
   
  def newpositions(self,dt=.005):
    self.xpos = self.xpos+self.xvel*dt*1000
    self.ypos = self.ypos+self.yvel*dt*1000

    #simple friction, it is wrong, but oh well
    friction_coefficient = .588 #.06 * 9.8
    friction_coefficient = 1
    self.vel = self.vel-friction_coefficient*dt
    self.vel[self.vel<0]=0
    self.vttoxy()
  
  def twobodycolision(self,b1,b2): #b1 and b2 are indecies of which balls are coliding.
    #calculating contact angle
    self.xytovt()
    dx = self.xpos[b2]-self.xpos[b1]
    dy = self.ypos[b2]-self.ypos[b1]
    phi = None #contact angle
    if dx==0:
      phi = np.pi/2
    else:
      phi = np.arctan2(dy,dx)

    #print(self.xvel[b1],self.yvel[b1],self.vel[b1],'|',self.xvel[b2],self.yvel[b2],'|',phi,'|',self.theta[b1],self.theta[b2])

    #source: https://en.wikipedia.org/wiki/Elastic_collision
    
    xb1= self.vel[b2]*np.cos(self.theta[b2] - phi)*np.cos(phi) + self.vel[b1]*np.sin(self.theta[b1]-phi)*np.cos(phi+np.pi/2)
    
    yb1 = self.vel[b2]*np.cos(self.theta[b2] - phi)*np.sin(phi) + self.vel[b1]*np.sin(self.theta[b1]-phi)*np.sin(phi+np.pi/2)
    
    self.xvel[b2] = self.vel[b1]*np.cos(self.theta[b1] - phi)*np.cos(phi) + self.vel[b2]*np.sin(self.theta[b2]-phi)*np.cos(phi+np.pi/2)
    
    self.yvel[b2] = self.vel[b1]*np.cos(self.theta[b1] - phi)*np.sin(phi) + self.vel[b2]*np.sin(self.theta[b2]-phi)*np.sin(phi+np.pi/2)
    self.xvel[b1] = xb1
    self.yvel[b1] = yb1
    self.xytovt()

  def findcollisions(self):
    points = 0
    for i in range(len(self.xpos)-1):
      #need to fix in case of multiple balls on collision
      if self.xpos[i]>0:


        d = np.sqrt(np.square(self.xpos-self.xpos[i])+np.square(self.ypos-self.ypos[i]))
        #need to fix for multi-body
        for j in range(i+1,len(self.xpos)):
          if d[j]<=57.15:

            #determining if balls are traveling apart or together, probably slow, need to fix
            dvec = np.array([self.xpos[i]-self.xpos[j],self.ypos[i]-self.ypos[j]])
            vvec = np.array([self.xvel[j]-self.xvel[i],self.yvel[j]-self.yvel[i]])
            anglebetween = np.arccos( np.dot( dvec/mynorm(dvec), vvec / mynorm(vvec)))
            if anglebetween<np.pi/2: #balls are colliding
              self.twobodycolision(i,j)

              #points
              if i==0 and self.firstCollision: #cue ball strike
                self.firstCollision=False
                if j<8:
                  points+=5
                  self.canContinue=True
                elif j>8:
                  self.canContinue=False
                  points-=2
                elif self.xpos[1:8].sum()==-700: #black ball collided, only ball left
                  points+=5
                  self.canContinue=True
                else: #black ball collided, other balls left
                  self.canContinue=False
                  points-=2
    return points

  def printpos(self,outfile):
    for i in range(len(self.xpos)):
      print(self.xpos[i],self.ypos[i],file=outfile)
    #print debug screen
    print(self.xvel[0],self.vel[1],self.vel[2],file=outfile)