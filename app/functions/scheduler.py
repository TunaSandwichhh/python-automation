import sched
import time
import threading

class Scheduler:
    def __init__(self, reminder_instance, interval=60):
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.reminder_instance = reminder_instance
        self.interval = interval 

    def run(self):
        self._schedule_next_event()
        t = threading.Thread(target=self._run_scheduler)
        t.daemon = True 
        t.start()

    def _run_scheduler(self):
        try:
            self.scheduler.run()
        except Exception as e:
            print(f"An error occurred in the scheduler: {e}")

    def _schedule_next_event(self):
        self.scheduler.enter(self.interval, 1, self._check_and_send_reminders)

    def _check_and_send_reminders(self):
        try:
            print("Checking for due tasks...")
            self.reminder_instance.send_reminders()
        except Exception as e:
            print(f"An error occurred while sending reminders: {e}")
        finally:
            self._schedule_next_event()