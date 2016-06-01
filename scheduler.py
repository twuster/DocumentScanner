"""
Scheduler that runs the document scanner job every minute
"""
import schedule
import time

from runner import Runner


def run():
    print("Running")

schedule.every().minute.do(run)
schedule.every().minute.do(Runner.run)

while True:
    schedule.run_pending()
    time.sleep(1)