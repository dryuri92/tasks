import random
import pytest
from typing import Generator, Tuple
from model import Task, Resources, TaskQueue

def id_generator()->Generator[int, int, int]:
    i = 0
    while True:
        yield i
        i += 1
        
@pytest.fixture
def task_queue():
    return TaskQueue()

@pytest.fixture
def filled_task_queue(task_queue):
    task_queue.add_task(Task(id=1,
                priority=1,
                resources=Resources(2,4,0),
                content=f"Task 1"))
    task_queue.add_task(Task(id=2,
                priority=1,
                resources=Resources(2,4,0),
                content=f"Task 2"))
    task_queue.add_task(Task(id=3,
                priority=2,
                resources=Resources(2,4,0),
                content=f"Task 3"))
    task_queue.add_task(Task(id=4,
                priority=1,
                resources=Resources(2,4,0),
                content=f"Task 4"))
    return task_queue

@pytest.fixture
def ranges()->Tuple[range, range, range, range]:
    # Define the ranges for task attributes
    priority_range = range(1, 100)
    cpu_range = range(1, 64)
    ram_range = range(1, 256)
    gpu_range = range(0, 256)
    return priority_range, \
    cpu_range, \
    ram_range, \
    gpu_range

@pytest.fixture
def available_resources():
    return Resources(ram=8, cpu_cores=4, gpu_count=1)

@pytest.fixture
def invalid_task():
    return Task(id=1, priority=1, resources=Resources(ram=300, cpu_cores=100, gpu_count=500), content="Invalid Task")

@pytest.fixture
def valid_task():
    return Task(id=1, priority=1, resources=Resources(ram=4, cpu_cores=2, gpu_count=1), content="Valid Task")

def generate_resources(
        cpu_range: range,
        ram_range: range,
        gpu_range: range,
        )->Resources:
    ram = random.randint(ram_range.start, ram_range.stop)
    cpu_cores = random.randint(cpu_range.start, cpu_range.stop)
    gpu_count = random.randint(gpu_range.start, gpu_range.stop)
    return Resources(
        ram=ram,
        cpu_cores=cpu_cores, 
        gpu_count=gpu_count)

def generate_tasks(
        taskid: int,
        priority_range: range,
        cpu_range: range,
        ram_range: range,
        gpu_range: range,
        )->Task:
    resource = generate_resources(cpu_range=cpu_range,
                                  ram_range=ram_range,
                                  gpu_range=gpu_range)
    task = Task(id=taskid,
                priority=random.randint(priority_range.start, priority_range.stop),
                resources=resource,
                content=f"taskid{taskid}")
    return task

def test_get_correct_task(filled_task_queue, available_resources):
    t = filled_task_queue.get_task(available_resources)
    assert t
    assert t.content == "Task 3"
    assert len(filled_task_queue.queue) == 3

def test_validate_task(invalid_task, valid_task, task_queue):
    assert not task_queue.validate_task(invalid_task)
    assert task_queue.validate_task(valid_task)

def test_add_task_invalid(invalid_task, task_queue):
    with pytest.raises(ValueError):
        task_queue.add_task(invalid_task)

def test_add_task_valid(valid_task, task_queue):
    task_queue.add_task(valid_task)
    assert len(task_queue.queue) == 1

def test_get_task_empty(task_queue, available_resources):
    assert task_queue.get_task(available_resources) == None

def test_get_task_valid(valid_task, task_queue, available_resources):
    task_queue.add_task(valid_task)
    assert task_queue.get_task(available_resources) == valid_task
    assert len(task_queue.queue) == 0

def test_get_task_no_match(task_queue, available_resources):
    task = Task(
        id=2, 
        priority=1, 
        resources=Resources(ram=16, cpu_cores=8, gpu_count=2), content="High Resource Task")
    task_queue.add_task(task)
    assert task_queue.get_task(available_resources) == None
    assert len(task_queue.queue) == 1

def test_load_task(ranges):
    queue = TaskQueue()
    generator = id_generator()
    for _ in range(1000000):
        t = generate_tasks(
            next(generator),
            ranges[0],
            ranges[1],
            ranges[2],
            ranges[3]
        )
        print(f" task i is {t}")
        queue.add_task(t)
    r = Resources(ram=32, cpu_cores=32, gpu_count=32)
    task = queue.get_task(r)
    print(f"task for this condition {task}")
    assert task != None

           
