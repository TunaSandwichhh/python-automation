class Task:
    def __init__(self, task_id, description, due_date, status=0):
        self.task_id = task_id
        self.description = description
        self.due_date = due_date
        self.status = status  # 0 for not notified, 1 for notified

    def __repr__(self):
        return f"Task(task_id={self.task_id}, description='{self.description}', due_date='{self.due_date}', status={self.status})"

    def mark_as_notified(self):
        self.status = 1

    def to_dict(self):
        return {
            'task_id': self.task_id,
            'description': self.description,
            'due_date': self.due_date,
            'status': self.status
        }

    @staticmethod
    def from_dict(data):
        return Task(
            task_id=data.get('task_id'),
            description=data['description'],
            due_date=data['due_date'],
            status=data.get('status', 0)
        )