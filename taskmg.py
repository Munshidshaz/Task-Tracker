#imports json,os,arug,datetime
import json
import os
import argparse
from datetime import datetime

#function get systemtime
def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


#function for read json file
def read_tasks():
    if os.path.exists('task3.json'):
        try:
            with open('task3.json','r') as tasks:
                content= json.load(tasks)
            if not content:
                return []
            return content
        except (json.JSONDecodeError,FileExistsError):
            return []
    return []

#function write file
def write_file(file):
    with open('task3.json','w') as f:
        json.dump(file,f,indent=3)  


#function for writing to json file
def save_tasks(description,status):
    tasks=read_tasks()
    nextid=max((task['id']for task in tasks),default=0)+1
    timenow=current_time()
    new_task={
        'id':nextid,
        'description': description,
        'status': status,
        'createat': timenow,
        'updateat' : timenow
    }
    tasks.append(new_task)
    write_file(tasks)
    

#function for search task
def update_task(id, description, status):
    """Finds a task by its ID and updates its description and/or status."""
    tasks = read_tasks()
    task = next((t for t in tasks if t['id'] == id), None)

    if task is None:
        print(f"Error: Task with ID {id} not found.")
        return

    updated = False
    if description is not None:
        task['description'] = description
        updated = True
    
    if status is not None:
        task['status'] = status
        updated = True

    if updated:
        task['updateat'] = current_time()
        write_file(tasks)
        print(f"Task {id} updated successfully.")
    else:
        print("No new information provided to update. Please provide --description or --status.")

#delete function 
def delete_task(id):
    tasks=read_tasks()
    task = next((task for task in tasks if task['id']==id),None)
    if task is None:
        print(f"Error: Task with ID {id} not found.")
        return
    tasks.remove(task)
    write_file(tasks)
    print(f"Task {id} has been deleted successfully.")

#function for listing task
def list_tasks(status=None):
    tasks=read_tasks()
    if not tasks:
        print("Your task list is empty! Go add something to do.")
        return

    print("-" * 80)
    print("                              --- Your Tasks ---")
    print("-" * 80)
    print(f"{'ID':<5} | {'Status':<10} | {'Created At':<20} | {'Description'}")
    print("-" * 80)
    
    tasks_to_show = [t for t in tasks if status is None or t['status'] == status]

    if not tasks_to_show:
        if status:
            print(f"No tasks with status '{status}' found.")
    else:
        for task in tasks_to_show:
            print(f"{task['id']:<5} | {task['status']:<10} | {task['createat']:<10} | {task['description']}")
    
    print("-" * 80)

#use argparser to take input
parser=argparse.ArgumentParser(description="A program to manage tasks")
#argparser add_parser for --mode
parser.add_argument("--mode", required=True,help="The operation mode (e.g., add, list, update, delete).")
parser.add_argument("--id", type=int, help="The ID of the task to update or delete.")
#argparser add_parser for --description
parser.add_argument("--description",help="The task description.",default=None)
#argparser add_parser for --status
parser.add_argument("--status",help="The status of the task")

args = parser.parse_args()


#if --mode == create:
if args.mode == 'create':
    if not args.description:
        print("Error: A description is required to create a task. Use --description 'Your task'.")
    else:
        save_tasks(args.description,args.status)

#if --mode == list:
if args.mode == 'list':
    list_tasks(args.status)
    
#if --mode == update:
if args.mode == 'update':
    if not args.id:
        print("Error: An ID is required to update a task. Use --id <task_id>.")
    elif not args.description and not args.status:
        print("Error: You must provide a new --description or --status to update.")
    else:
        update_task(args.id, args.description, args.status)

#if --mode == delete:
if args.mode == 'delete':
    if not args.id:
        print("Error: An ID is required to delete a task. Use --id <task_id>.")
    else:
        delete_task(args.id)




