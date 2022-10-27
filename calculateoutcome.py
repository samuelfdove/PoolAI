
import numpy as np
from matplotlib import pyplot as plt
import cProfile
import math
import timeit
import copy

def mynorm(a):
  return math.sqrt(a[0]**2+a[1]**2)

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
            reward-=10
            self.canContinue=False
          elif i>0 and i<8:
            reward+=10
            if self.canContinue==None:
              self.canContinue==True
          elif i>8:
            reward-=5
          elif i==8:
            if B.xpos[1:8].sum()==-700:
              reward+=20
              self.canContinue=True
            else:
              reward-=100
              self.canContinue=False
    return reward
          
          

class Turn(object):
  def __init__(self,ballpos,holecords=[[110,113],[1181,72],[2262,114],[2240,1134],[1181,1188],[112,1147]],wallcords=[[111,178],[0,178],[0,0],[174,0],[174,103],[217,142],[1106,142],[1124,105],[1124,0],[1237,0],[1237,103],[1255,142],[2152,142],[2198,103],[2198,0],[2389,0],[2390,177],[2278,177],[2235,218],[2235,1040],[2279,1082],[2389,1082],[2389,1259],[2198,1259],[2197,1156],[2153,1116],[1256,1116],[1237,1155],[1237,1259],[1125,1259],[1125,1155],[1107,1116],[220,1116],[177,1155],[177,1259],[0,1259],[0,1082],[111,1082],[153,1040],[153,218]]):
    global br
    br = 57.15 #need to change
    global be
    be = 1

    self.w = Walls(wallcords)
    self.h = Holes(holecords)

    self.initialstate=ballpos
    


  def taketurn(self,xvel,yvel):
    b = Balls(self.initialstate)
    b.strikecuexy(xvel,yvel)
    log = False
    reward=0
    if log:
      global outfile
      outfile = open('outputtext.txt','w')
    while b.vel.sum()>0:
      b.newpositions()
      self.reward+=self.h.intoholes(b)
      self.reward+=b.findcollisions()
      
      if log:
        b.printpos(outfile)

      self.w.wallcollision(b)

    
    if self.h.canContinue==True and b.canContinue==True:
      done=False
    else:
      done=True
    self.h.canContinue=None

    finalstate = np.array([b.xpos,b.ypos]).transpose()

    return [finalstate,reward,done]


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