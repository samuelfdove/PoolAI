from pygamesim import main as pygamemain
from findballpos import findballpos
from Turn import *
from Balls import *
import random

# t = Turn()
# while True:
#   t.reset()
#   print(t.ballstate)
#   t.taketurn(random.randint(1000,2500)/1000,random.randint(1000,2500)/1000)
#   #t.taketurn(3,3)
#   pygamemain()

print(np.asarray(findballpos()))
print(
  Balls(np.asarray(findballpos()))
)