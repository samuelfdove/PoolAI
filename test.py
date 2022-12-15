from pygamesim import main as pygamemain
from findballpos import findballpos
from Turn import *
import random

while True:
  t = Turn(findballpos())
  print(t.initialstate)
  # t.taketurn(random.randint(0,2500)/1000,random.randint(0,2500)/1000)
  t.taketurn(.1,.1)
  pygamemain()

