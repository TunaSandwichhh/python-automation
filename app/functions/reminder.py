import datetime

class Reminder:
    def __init__(self, task_db, notification_system, log_db):
        self.task_db = task_db
        self.notification_system = notification_system
        self.log_db = log_db

    def send_reminders(self):
        try:
            tasks = self.task_db.get_all_tasks()
            for task in tasks:
                if self._is_task_due(task) and task['status'] == 0:
                    self._send_reminder(task)
        except Exception as e:
            print(f"Error when sending reminders: {e}")

    def _is_task_due(self, task):
        try:
            due_date = datetime.datetime.strptime(task['due_date'], '%Y-%m-%d %H:%M:%S')
            current_time = datetime.datetime.now()
            return due_date <= current_time
        except Exception as e:
            print(f"Error when checking if task is due: {e}")
            return False 

    def _send_reminder(self, task):
        try:
            to_number = task['to_number']
            message = f"Reminder: Your task '{task['description']}' is due on {task['due_date']}."
            success, message_sid = self.notification_system.send_sms(to_number, message)

            sent_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if success:
                self.task_db.update_task(task['id'], task['description'], task['due_date'], 1)
                self.log_db.log_notification(task['id'], 'sms', sent_datetime, 'sent', message_sid)
            else:
                self.log_db.log_notification(task['id'], 'sms', sent_datetime, 'failed', None)
        except Exception as e:
            print(f"Error when sending a reminder for task ID {task['id']}: {e}")
            sent_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.log_db.log_notification(task['id'], 'sms', sent_datetime, 'error', None)