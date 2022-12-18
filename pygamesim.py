import pygame

def main():
  pygame.init()
  myFont = pygame.font.SysFont("Times New Roman", 18)
  (width,height) = (1700,1000)
  #(width,height) = (1195,630)
  screen = pygame.display.set_mode((width,height))
  table = pygame.image.load('poolassets/table.png')
  table = pygame.transform.scale(table,(width,height))
  log = open('outputtext.txt','r')
  balls = []
  #4551,2570
  #145,141
  scalex = width/4551
  scaley = height/2570

  ballsizex = 4257/2235*57.15*scalex
  ballsizey = 2277/1118*57.15*scaley
  ballshiftx = ballsizex/2
  ballshifty = ballsizey/2


  for i in range(16):
      fname = "poolassets/ball_"+str(i)+".png"
      ball = pygame.image.load(fname)
      # ball = pygame.transform.scale(ball,(145*scalex,141*scaley))
      ball = pygame.transform.scale(ball,(ballsizex,ballsizey))
      balls.append(ball)


  running = True
  while running:
    for event in pygame.event.get():
      
      numprints = 17
      screen.blit(table,(0,0))
      poss = log.readlines()
      for j in range(len(poss)//numprints):
        screen.blit(table,(0,0))
        message = ''
        for i in range(numprints):
          #screen.blit(table,(0,0))
          #size (in mm) 2235,1118
          #size (in px) 4257,2277
          pos = poss[j*numprints+i].split(' ')
          #+239
          if i<=15: #its a ball
            ballx = (float(pos[0]) / 2235 * 4257)*scalex-ballshiftx
            bally = (float(pos[1]) / 1118 * 2277)*scaley-ballshifty
            screen.blit(balls[i],(ballx,bally))
          else: #debug display
            message = poss[j*numprints+i]

            display = myFont.render(message, 1, (0,0,0))

            #screen.blit(display,(500+50*(i-17),500+50*(i-17)))
            
          

          
          
            

          
        for event in pygame.event.get():
          pass 
        #mx,my = pygame.mouse.get_pos()
        
        #screen.blit(myFont.render(str(mx),1,(0,0,0)),(800,800))
        pygame.display.flip()
        if message!='\n':
          pygame.time.delay(1)
        pygame.time.delay(50)
        
        if event.type == pygame.QUIT:

          running = False
      running=False

#main()