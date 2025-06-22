import json
import os
from datetime import datetime, timedelta
from collections import defaultdict


class SmartTodoList:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()
        
    def add_task(self, title, category="general", priority=3, due_date=None):
        """Добавление новой задачи"""
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "category": category,
            "priority": priority,  # 1: highest, 5: lowest
            "due_date": due_date,
            "created": datetime.now().isoformat(),
            "completed": False
        }
        self.tasks.append(task)
        self.save_tasks()
        return task

    
    def complete_task(self, task_id):
        """Отметка задачи как выполненной"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                task["completed_at"] = datetime.now().isoformat()
                self.save_tasks()
                return True
        return False

    def get_pending_tasks(self):
        """Получение списка активных задач"""
        return [task for task in self.tasks if not task["completed"]]
    