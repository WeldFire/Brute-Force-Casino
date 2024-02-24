import json
from Casinos.Chumba import Chumba
from enums.CasinoEnum import CasinoEnum
from Casinos.GlobalPoker import GlobalPoker
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from enum import Enum
import sys
import time
import logging


class RunSchedule(Enum):
  SixHours = 6
  EveryHour = 1
  All = 0

  def isCompatibleWithRunSchedule(self, testedRunSchedule):
      return testedRunSchedule == RunSchedule.All or testedRunSchedule == self

def load_configuration():
    # Open and load the JSON file
    with open('config.json', 'r') as file:
        map_var = json.load(file)
        
    #print(map_var)
    return map_var

async def main(schedule = RunSchedule.All):
    #gp = GlobalPoker(CONFIGURATION.get(CasinoEnum.GLOBALPOKER.value))
    #await gp.claim()

    #TODO: on hold until I can figure out how to intercept emails to get the code then fill it in
    chumba = Chumba(CONFIGURATION.get(CasinoEnum.CHUMBA.value))
    await chumba.claimChumba2()




def startup(schedule = RunSchedule.All):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        asyncio.run(main(schedule))
    except KeyboardInterrupt:
        pass


CONFIGURATION = load_configuration()

if __name__ ==  '__main__':
    run_schedule = RunSchedule.All
    if len(sys.argv) > 1:
        run_schedule_raw = sys.argv[1].lower()
        if run_schedule_raw == "hourly":
            run_schedule = RunSchedule.EveryHour
        elif run_schedule_raw == "six-hours":
            run_schedule = RunSchedule.SixHours

    startup(run_schedule)
    
    scheduler = BackgroundScheduler()
    if(RunSchedule.EveryHour.isCompatibleWithRunSchedule(run_schedule)):
        scheduler.add_job(lambda schedule = RunSchedule.EveryHour: startup(schedule), 'interval', hours=1, minutes=2)

    if(RunSchedule.SixHours.isCompatibleWithRunSchedule(run_schedule)):
        scheduler.add_job(lambda schedule = RunSchedule.SixHours:  startup(schedule), 'interval', hours=6, minutes=2)
    
    scheduler.start()
    
    try:
        while 1:
            # Do nothing since blocking scheduler is brok.... zzzz
            time.sleep(0.1)
    except (KeyboardInterrupt, SystemExit):
        logging.warning('Got SIGTERM! Terminating...')
        scheduler.shutdown(wait=False)
