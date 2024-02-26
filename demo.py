""" This code just for demonstration purporse only.
    It will print out task satisfied the avaiable resources:
    `python3 demo.py`
"""
from model import *

if __name__ == '__main__':
    task1 = Task(id=1, priority=2, resources=Resources(ram=4, cpu_cores=2, gpu_count=1), content="Task 1")
    task2 = Task(id=2, priority=1, resources=Resources(ram=6, cpu_cores=3, gpu_count=1), content="Task 2")
    task3 = Task(id=3, priority=3, resources=Resources(ram=2, cpu_cores=1, gpu_count=1), content="Task 3")
    task4 = Task(id=4, priority=4, resources=Resources(ram=256, cpu_cores=1, gpu_count=1), content="Task 4")
    tq = TaskQueue()
    tq.add_task(task1)
    tq.add_task(task2)
    tq.add_task(task3)
    resource = Resources(ram=16, cpu_cores=8, gpu_count=2)
    task = tq.get_task(resource)
    #sorted(tq.queue, key=lambda x: x.priority)
    print(f"for avaiable resources {resource} task found:{task}")
