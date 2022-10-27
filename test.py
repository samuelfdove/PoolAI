from pygamesim import main as pygamemain
from findballpos import findballpos
from calculateoutcome import *
import random

while True:
  t = Turn(findballpos())
  t.taketurn(random.randint(0,2500)/1000,random.randint(0,2500)/1000)
  pygamemain()
