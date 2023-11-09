import os
import time
from dotenv import load_dotenv
from app.db.task_database import TaskDatabase
from app.db.notification_log_database import NotificationLogDB
from app.functions.notification import Notification
from app.functions.reminder import Reminder
from app.functions.scheduler import Scheduler

import datetime

def main():
    load_dotenv()

    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    twilio_number = os.getenv('TWILIO_NUMBER')

    task_db_path = os.getenv('TASK_DB_PATH', 'tasks.db')
    notification_log_db_path = os.getenv('NOTIFICATION_LOG_DB_PATH', 'notifications.db')

    task_db = TaskDatabase(task_db_path)
    log_db = NotificationLogDB(notification_log_db_path)

    notification_system = Notification(account_sid, auth_token, twilio_number)

    reminder = Reminder(task_db, notification_system, log_db)

    scheduler = Scheduler(reminder, interval=60)
    scheduler.run()

    try:
        print("Reminder system is running. Press Ctrl+C to exit.")
        while True:
            print("\nCommand Menu:")
            print("1 - Add new task")
            print("2 - View all tasks")
            print("3 - Delete a task")
            print("4 - Trigger reminder check manually")
            print("5 - Exit")
            command = input("Enter command: ")

            if command == "1":
                description = input("Enter task description: ")
                due_date = input("Enter due date (YYYY-MM-DD HH:MM:SS): ")
                to_number = input("Enter recipient's phone number for SMS notification: ")
                task_db.add_task(description, due_date, to_number)
                print("Task added.")
            
            elif command == "2":
                tasks = task_db.get_all_tasks()
                for task in tasks:
                    print(task)
            
            elif command == "3":
                task_id = input("Enter task ID to delete: ")
                task_db.delete_task(task_id)
                print(f"Task {task_id} deleted.")
            
            elif command == "4":
                reminder.send_reminders()
                print("Manual reminder check completed.")
            
            elif command == "5":
                raise KeyboardInterrupt
            
            else:
                print("Invalid command. Please try again.")
            
            time.sleep(1) 

    except KeyboardInterrupt:
        print("Application stopped by the user.")
    finally:
        task_db.close_connection()
        log_db.close_connection()
        print("Database connections closed.")

if __name__ == '__main__':
    main()