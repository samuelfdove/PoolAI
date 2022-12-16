from pygamesim import main as pygamemain
from findballpos import findballpos
from Turn import *
import random

while True:
  t = Turn()
  print(t.ballstate)
  # t.taketurn(random.randint(0,2500)/1000,random.randint(0,2500)/1000)
  t.taketurn(3,3)
  pygamemain()

