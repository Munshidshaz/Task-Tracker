import json
import os
import argparse

def file_reader():
    if os.path.exists("tasks.json"):
         with open("tasks.json","r") as f:
            return json.load(f)
    else:
        return []

def save_data(data):
    with open("tasks.json","w") as f:
        json.dump(data, f, indent=4)


def create_task(description, status):
    tasks = file_reader()
    maxid = max((x['id']for x in tasks),default=0)+1
    new_task={
        'id': maxid,
        'description':description,
        'status':status
    }
    tasks.append(new_task)
    save_data(tasks)
    print("Data saved")

parser = argparse.ArgumentParser(description="Task Tracker")
parser.add_argument("--command",help="Enter the command mode")
parser.add_argument("--description", help="Enter the description")
parser.add_argument("--status",help="Status of the task")
parser.add_argument("--id", help="Id of the task")

args = parser.parse_args()

if args.command == 'add' and args.description:
    create_task(args.description,args.status or 'Pending')

if args.command == 'list':
    tasks=file_reader()
    if args.status==None:
        for task in tasks:
            print(f"ID: {task['id']}, Task: {task['description']}, Status: {task['status']}")
    if args.status:
        for task in tasks:
            if task['status']==args.status:
                print(f"ID: {task['id']}, Task: {task['description']}, Status: {task['status']}")


if args.command == 'delete':
    tasks=file_reader()
    tasks=[item for item in tasks if item['id'] != int(args.id)]
    save_data(tasks)

if args.command == 'update' :
    tasks=file_reader()
    for task in tasks:
        if task['id'] == int(args.id):
            if args.description:
                task['description'] = args.description
            if args.status:
                task['status'] = args.status
            break
    save_data(tasks)
