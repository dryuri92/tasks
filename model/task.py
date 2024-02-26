from dataclasses import dataclass
from typing import List
from collections import deque

# Constants for resource limits
LOW_GPU_VALUE = 0
HIGH_GPU_VALUE = 256
LOW_CPU_VALUE = 1
HIGH_CPU_VALUE = 64
LOW_RAM_VALUE = 1
HIGH_RAM_VALUE = 256

@dataclass
class Resources:
    ram: int
    cpu_cores: int
    gpu_count: int

@dataclass
class Task:
    id: int
    priority: int
    resources: Resources
    content: str
    result: str = ""

class TaskQueue:
    def __init__(self):
        # Initialize the queue as a list
        self.queue: List[Task] = list()

    # Method to validate if a task's resources are within acceptable ranges
    def validate_task(self, task: Task) -> bool:
        """Validate if a task's resources are within acceptable ranges."""
        if (task.resources.cpu_cores > HIGH_CPU_VALUE) or (task.resources.cpu_cores < LOW_CPU_VALUE):
            return False
        if (task.resources.gpu_count > HIGH_GPU_VALUE) or (task.resources.gpu_count < LOW_GPU_VALUE):
            return False
        if (task.resources.ram > HIGH_RAM_VALUE) and (task.resources.ram < LOW_RAM_VALUE):
            return False
        return True
    
    # Method to add a task to the queue
    def add_task(self, task: Task):
        """Add a task to the queue."""
        if not self.validate_task(task):  # Check if the task is valid
            raise ValueError(f"Task not valid: {task}")
        self.queue.append(task)  # Add the task to the queue

    # Method to get a task from the queue based on available resources
    def get_task(self, available_resources: Resources) -> Task:
        """Get a task from the queue based on available resources."""
        for task in sorted(self.queue, key=lambda x: x.priority, reverse=True):
            if (task.resources.ram <= available_resources.ram and
                    task.resources.cpu_cores <= available_resources.cpu_cores and
                    task.resources.gpu_count <= available_resources.gpu_count):
                self.queue.remove(task)  # Remove the task from the queue
                return task
        return None  # Return None if no suitable task is found