from phaseshift import db
from phaseshift.models import Events
def addevent():
  name = input('name: ')
  etype = input('type: ')
  dept = input('dept: ')
  desc = input('desc: ')
  fee =  int(input('fee'))
  team_size = int(input('teame: '))
  date = input('date: ')
  time = input('time: ')
  venue = input('venue: ')
  coordinators = input('cords: ')
  prize = input('prize: ')
  workshop = input('workshop: ')
  flagship = input('flagship: ')

  if workshop=='0':
    workshop=False
  else:
    workshop=True
  if flagship=='0':
    flagship=False
  else:
    flagship=True
  
  E = Events(name=name, etype=etype,dept=dept,desc=desc,fee=fee,team_size=team_size,date=date,time=time,venue=venue,coordinators=coordinators,prize=prize,workshop=workshop,flagship=flagship)
  db.session.add(E)
  db.session.commit()

def startevents():
  while(True):
    addevent()
    ch = input('Continue: ')
    if ch == 'stop':
      break

def checkevents():
  al = Events.query.all()
  for x in al:
    print(x)

while True:
  startevents()
  ch = input('Check events? ')
  if ch == 'yes':
    checkevents()
  elif ch == 'no':
    break


 