import json
import os
import argparse
import datetime

def read_tasks():
    if os.path.exists('tasks3.json'):
        try:
            with open('task3.json','r') as tasks:
                return json.load(tasks)
        except FileExistsError:
            return []
read_tasks()