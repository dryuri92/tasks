from dataclasses import dataclass
from collections import deque
from typing import List
#Constant value for resources
LOW_GPU_VALUE=0
HIGH_GPU_VALUE=256
LOW_CPU_VALUE=1
HIGH_CPU_VALUE=64
LOW_RAM_VALUE=1
HIGH_RAM_VALUE=256

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
        self.queue: List[Task] = list()

    def validate_task(self, task: Task)->bool:
        if (task.resources.cpu_cores > HIGH_CPU_VALUE) or (task.resources.cpu_cores < LOW_CPU_VALUE):
            return False
        if (task.resources.gpu_count > HIGH_GPU_VALUE) or (task.resources.gpu_count < LOW_GPU_VALUE):
            return False
        if (task.resources.ram > HIGH_RAM_VALUE) and (task.resources.ram < LOW_RAM_VALUE):
            return False
        return True
    
    def add_task(self, task: Task):
        if (not self.validate_task(task)):
            raise ValueError(f"Task not valide: {task}")
        self.queue.append(task)

    def get_task(self, available_resources: Resources) -> Task|None:
        for task in sorted(self.queue, key = lambda x: x.priority, reverse=True):
            if (task.resources.ram <= available_resources.ram and
                    task.resources.cpu_cores <= available_resources.cpu_cores and
                    task.resources.gpu_count <= available_resources.gpu_count):
                self.queue.remove(task)
                return task
        return None
