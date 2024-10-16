"""TASKS"""
from queue import Queue
import os
from threading import Thread, Lock

class ThreadPool:
    """THREAD POOL"""
    def __init__(self, data, data_dict, questions_best_is_min, logger):
        """
        Initialize the ThreadPool object

        Parameters:
            data : Csv data
            data_dict : Dictionary containing index data for tasks
            questions_best_is_min : List of questions for which lower values are considered better
            logger : Logger object for logging events
        """
        self.questions_best_is_min = questions_best_is_min
        self.logger = logger
        self.data_dict = data_dict
        self.task_queue = Queue()
        self.thread_list = []
        self.tasks_finished = {}
        self.finish_lock = Lock()
        self.up = 1
        if "TP_NUM_OF_THREADS" in os.environ:
            self.nr_threads = os.environ["TP_NUM_OF_THREADS"]
        else:
            self.nr_threads = os.cpu_count()
        i = 0
        while i < self.nr_threads:
            self.thread_list.append(TaskRunner(data, self.tasks_finished,
                                               data_dict,
                                                self))
            i += 1
    def start(self):
        """Start all threads in the thread pool"""
        for i in range(self.nr_threads):
            self.thread_list[i].start()
        self.logger.info("Threads started")
    def stop(self):
        """Stop all threads in the thread pool"""
        i = 0
        self.up = 0
        while i < self.nr_threads:
            self.task_queue.put(["exit"])
            i += 1
        i = 0
        while i < self.nr_threads:
            self.thread_list[i].join()
            i += 1
        self.logger.info("Threads stopped")
    def add_task(self, vect_in):
        """Add a new task to the thread pool"""
        #Started a new task
        if self.up:
            with self.finish_lock:
                self.tasks_finished[vect_in[1]] = {}
                self.logger.info(f"New task with job_id_{vect_in[1]}")
            self.task_queue.put(vect_in)
        else:
            self.logger.info("Tried to add a task after shutdown!")
            
class TaskRunner(Thread):
    """TASK RUNNER"""
    def __init__(self, data, tasks_finished, data_dict, threadpool):
        Thread.__init__(self)
        self.threadpool = threadpool
        self.data = data
        self.data_dict = data_dict
        self.tasks_finished = tasks_finished
    def run(self):
        while True:
            item = self.threadpool.task_queue.get()
            #STOP
            if item[0] == "exit":
                break
            #Question
            if item[0] == "question":
                self.questions(item[1:])
    def questions(self, vect_in):
        """Process task with question type
        
            Parameters:
                vect_in[0] = job_id
                vect_in[1] = api type
                vect_in[2] = question
                vect_in[3] = state
        """
        self.threadpool.logger.info(f"Processing task with job_id_{vect_in[0]}")
        if vect_in[1] == "1":
            out = self.states_mean_task(vect_in[2:])
        elif vect_in[1] == "2":
            out = self.state_mean_task(vect_in[2:])
        elif vect_in[1] == "3":
            out = self.best5(vect_in[2:])
        elif vect_in[1] == "4":
            out = self.worst5(vect_in[2:])
        elif vect_in[1] == "5":
            out = self.global_mean(vect_in[2:])
        elif vect_in[1] == "6":
            out = self.diff_from_mean(vect_in[2:])
        elif vect_in[1] == "7":
            out = self.state_diff_from_mean(vect_in[2:])
        elif vect_in[1] == "8":
            out = self.mean_by_category(vect_in[0:])
        elif vect_in[1] == "9":
            out = self.state_mean_by_category(vect_in[2:])
        #Write the result in the job_id file
        file = open("results/out_" + str(vect_in[0]) + ".txt", "w")
        file.write(str(out))
        file.close()
        #Finished a task
        with self.threadpool.finish_lock:
            self.tasks_finished[vect_in[0]] = out
            self.threadpool.logger.info(f"Finished task with job_id_{vect_in[1]}")

    def states_mean_task(self, vect_in):
        """/api/states_mean_task"""
        result = {}
        for key, state_dict in self.data_dict[vect_in[0]].items():
            summ = 0
            nr = 0
            for list_index in state_dict.values():
                for x in list_index:
                    summ += self.data["Data_Value"][x]
                nr += len(list_index)
            mean = float(summ/nr)
            result[key] = mean
        sorted_dict = dict(sorted(result.items(), key=lambda item: item[1]))
        return sorted_dict
    def state_mean_task(self,vect_in):
        """/api/state_mean_task"""
        summ = 0
        nr = 0
        state_dict = self.data_dict[vect_in[0]]
        for list_index in state_dict[vect_in[1]].values():
            for x in list_index:
                summ += self.data["Data_Value"][x]
            nr += len(list_index)
        mean = float(summ/nr)
        return {vect_in[1] : mean}
    def best5(self, vect_in):
        """/api/best5"""
        result = self.states_mean_task(vect_in)
        keys = list(result.keys())
        out = {}
        if vect_in[0] in self.threadpool.questions_best_is_min:
            for i in range(5):
                out[keys[i]] = result[keys[i]]
            return out
        last = len(keys)
        for i in range(5):
            out[keys[last-1-i]] = result[keys[last-1-i]]
        return out
    def worst5(self, vect_in):
        """/api/worst5"""
        result = self.states_mean_task(vect_in)
        keys = list(result.keys())
        out = {}
        last = len(keys)
        if vect_in[0] in self.threadpool.questions_best_is_min:
            for i in range(5):
                out[keys[last-1-i]] = result[keys[last-1-i]]
            return out
        for i in range(5):
            out[keys[i]] = result[keys[i]]
        return out
    def global_mean(self, vect_in):
        """/api/global_mean"""
        summ = 0
        nr = 0
        for state_dict in self.data_dict[vect_in[0]].values():
            for list_index in state_dict.values():
                for x in list_index:
                    summ += self.data["Data_Value"][x]
                    nr += 1
        mean = float(summ/nr)
        result = {"global_mean": mean}
        return result
    def diff_from_mean(self, vect_in):
        """/api/diff_from_mean"""
        result = {}
        total_summ = 0
        nr = 0
        for key, state_dict in self.data_dict[vect_in[0]].items():
            summ = 0
            nr_by_state = 0
            for list_index in state_dict.values():
                for x in list_index:
                    summ += self.data["Data_Value"][x]
                    nr += 1
                nr_by_state +=len(list_index)
            total_summ += summ
            mean = float(summ/nr_by_state)
            result[key] = mean
        total_summ = float (total_summ/nr)
        for key in result.keys():
            result[key] = total_summ - result[key]
        return result
    def state_diff_from_mean(self, vect_in):
        """/api/state_diff_from_mean"""
        return {vect_in[1] : self.global_mean(vect_in)["global_mean"]-
                self.state_mean_task(vect_in)[vect_in[1]]}
    def mean_by_category(self, vect_in):
        """/api/mean_by_category"""
        result = {}
        for state in self.data_dict[vect_in[2]].keys():
            aux = self.data_dict[vect_in[2]][state]
            for key in aux.keys():
                if str(key) == "nan":
                    continue
                summ = 0
                for index in aux[key]:
                    summ += self.data["Data_Value"][index]
                mean = float(summ/len(aux[key]))
                new_key = "('" + str(state) + "', '"
                new_key += str(self.data["StratificationCategory1"][aux[key][0]]) + "', '"
                new_key += str(key) + "')"
                result[new_key] = mean
        return result
    def state_mean_by_category(self, vect_in):
        """/api/state_mean_by_category"""
        result = {}
        for key, values in self.data_dict[vect_in[0]][vect_in[1]].items():
            summ = 0
            for x in values:
                summ += self.data["Data_Value"][x]
            mean = float(summ/len(values))
            new_key = "('" + self.data["StratificationCategory1"][values[0]] + "', '" + key + "')"
            result[new_key] = mean
        return {vect_in[1] : result}
