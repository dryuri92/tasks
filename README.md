## Task Queue

This is a simple task queue implementation in Python. It allows adding tasks with priorities and resource requirements to a queue and retrieving the highest priority task that satisfies the available resources.
It satisfies several conditions:
* Requires a task queue with priorities and resource limits.
* Each task has a priority and the required amount of resources to process it.
* Publishers create tasks with specified resource limits, and put them in a task queue.
* Consumer receives the highest priority task that satisfies available resources.
* The queue is expected to contain thousands of tasks.
* Write a unit test to demonstrate the operation of the queue.

## Installation

There's no installation necessary for this program. Just clone the repository or copy the code into your project.
Test are written on `pytest` framework to install it just type in console:
```sh
python3 -m pip install -r requirements.txt
```
or
```sh
pip  install -r requirements.txt
```
## Usage

1. Import the `TaskQueue`, `Task`, and `Resources` classes from the module.
2. Create a `TaskQueue` instance.
3. Add tasks to the queue using the `add_task` method.
4. Retrieve tasks from the queue based on available resources using the `get_task` method.

Example usage:

```python
from task_queue import TaskQueue, Task, Resources

# Create a TaskQueue instance
task_queue = TaskQueue()

# Define available resources
available_resources = Resources(ram=8, cpu_cores=4, gpu_count=1)

# Create a task
task1 = Task(id=1, priority=2, resources=Resources(ram=4, cpu_cores=2, gpu_count=1), content="Task 1")

# Add the task to the queue
task_queue.add_task(task1)

# Get a task based on available resources
selected_task = task_queue.get_task(available_resources)
