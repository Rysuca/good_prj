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

     def get_completed_tasks(self):
        """Получение списка выполненных задач"""
        return [task for task in self.tasks if task["completed"]]

    def analyze_habits(self, days=30):
        """Анализ привычек за указанный период"""
        cutoff = datetime.now() - timedelta(days=days)
        completed = [t for t in self.get_completed_tasks() 
                    if datetime.fromisoformat(t["completed_at"]) > cutoff]
        
        stats = {
            "total_completed": len(completed),
            "categories": defaultdict(int),
            "daily_completion": defaultdict(int),
            "priority_distribution": defaultdict(int)
        }
        
        for task in completed:
            stats["categories"][task["category"]] += 1
            day = datetime.fromisoformat(task["completed_at"]).strftime("%Y-%m-%d")
            stats["daily_completion"][day] += 1
            stats["priority_distribution"][task["priority"]] += 1
            
        return stats

    def upcoming_deadlines(self, days=7):
        """Получение предстоящих дедлайнов"""
        cutoff = datetime.now() + timedelta(days=days)
        return [task for task in self.get_pending_tasks() 
               if task["due_date"] and datetime.fromisoformat(task["due_date"]) <= cutoff]

    def save_tasks(self):
        """Сохранение задач в файл"""
        with open(self.filename, "w") as f:
            json.dump(self.tasks, f, indent=2)
    
def load_tasks(self):
        """Загрузка задач из файла"""
        if os.path.exists(self.filename):
            with open(self.filename) as f:
                self.tasks = json.load(f)

# Пример использования (демо)
if __name__ == "__main__":
    todo = SmartTodoList()
    
    # Добавление тестовых задач
    todo.add_task("Купить молоко", "покупки", 2)
    todo.add_task("Сделать упражнения", "здоровье", 1)
    todo.add_task("Прочитать книгу", "образование", 4, 
                 (datetime.now() + timedelta(days=3)).isoformat())
    
    # Завершение задачи
    todo.complete_task(1)
    
    # Аналитика
    print("Предстоящие дедлайны:")
    for task in todo.upcoming_deadlines():
        print(f"- {task['title']} (Приоритет: {task['priority']})")
    
    print("\nАнализ привычек:")
    stats = todo.analyze_habits()
    print(f"Всего выполнено: {stats['total_completed']}")
    print("По категориям:", dict(stats["categories"]))

    