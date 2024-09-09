import functools
import time
from collections import defaultdict

# Dictionary to store metrics for each function
metrics_store = defaultdict(lambda: {'calls': 0, 'errors': 0, 'total_time': 0.0})


class MetricsCollector:
    def __init__(self):
        self.metrics = {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            if func_name not in self.metrics:
                self.metrics[func_name] = {'num_calls': 0, 'total_time': 0.0, 'num_errors': 0, 'avg_time': 0.0}

            self.metrics[func_name]['num_calls'] += 1
            start_time = time.time()

            try:
                result = func(*args, **kwargs)
            except Exception as e:
                self.metrics[func_name]['num_errors'] += 1
                raise e
            finally:
                end_time = time.time()
                elapsed_time = end_time - start_time
                self.metrics[func_name]['total_time'] += elapsed_time
                self.metrics[func_name]['avg_time'] = self.metrics[func_name]['total_time'] / self.metrics[func_name][
                    'num_calls'] if self.metrics[func_name]['num_calls'] > 0 else 0
            return result

        return wrapper

    def get_metrics(self, func_name):
        if func_name in self.metrics:
            data = self.metrics[func_name]
            avg_time = data['total_time'] / data['num_calls'] if data['num_calls'] > 0 else 0
            return {
                'Function': func_name,
                'Number of calls': data['num_calls'],
                'Average execution time': avg_time,
                'Number of errors': data['num_errors'],
            }
        else:
            return f"No metrics found for function '{func_name}'"


# Create an instance of MetricsCollector
metrics_collector = MetricsCollector()
