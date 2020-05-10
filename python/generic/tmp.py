from threading import Thread
import os
class GenericInput:
    def read(self):
        raise NotImplemented
    @classmethod
    def generate_inputs(cls, config):
        raise NotImplemented

class PathInputData(GenericInput):
    def read(self):
        return open(self.path).read()
    def __init__(self, path):
        self.path = path
    @classmethod
    def generate_inputs(cls, config):
        data_dir = config["data_dir"]
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))

class GenericWorker(object):
    def __init__(self,  input_data):
        self.input_data = input_data
        self.result = None
    def map(self):
        raise NotImplemented
    def reduce(self, other):
        raise NotImplemented
    @classmethod
    def create_workers(cls, input_class, config):
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers

class  LineCountWorker(GenericWorker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count("\n")
        print("self.result", self.result)
    def reduce(self, other):
        self.result += other.result

def mapreduce(worker_class, input_class, config):
    workers =  worker_class.create_workers(input_class, config)
    return execute(workers)

def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads: thread.start()
    for thread in threads: thread.join()
    first, rest =  workers[0], workers[1:]
    for  worker in  rest:
        first.reduce(worker)
    return first.result

from tempfile import TemporaryDirectory
def write_test_files(tmpdir):
    for i in range(10):
        with open(f"{tmpdir}/{i}.txt", "w") as f:
            f.write("\n".join([str(j) for j in range(i)]))

with  TemporaryDirectory() as tmpdir:
    write_test_files(tmpdir)
    config = {"data_dir": tmpdir}
    result =  mapreduce(LineCountWorker, PathInputData, config)
    print(result)
