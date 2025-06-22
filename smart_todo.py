import json
import os
from datetime import datetime, timedelta
from collections import defaultdict


class SmartTodoList:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()
        