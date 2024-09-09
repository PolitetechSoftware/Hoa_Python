from celery_config import save_metrics_to_db
from create_db import create_db
from metrics_decorator import metrics_collector


@metrics_collector
def example_function():
    if True:  # Simulate a potential error
        raise ValueError("An example error")


@metrics_collector
def example_function2():
    return


if __name__ == "__main__":
    create_db()
    # Call the function multiple times
    for _ in range(1):  # Adjust the range as needed
        try:
            example_function()
        except ValueError as e:
            pass

    for _ in range(2):  # Adjust the range as needed
        try:
            example_function2()
        except ValueError as e:
            pass

    # Send metrics to Celery task for saving
    metrics_data = metrics_collector.metrics
    save_metrics_to_db.delay(metrics_data)

    # Retrieve and display metrics
    metrics = metrics_collector.get_metrics('example_function')
    print(f"Function: {metrics['Function']}")
    print(f"Number of calls: {metrics['Number of calls']}")
    print(f"Average execution time: {metrics['Average execution time']} seconds")
    print(f"Number of errors: {metrics['Number of errors']}")

    metrics = metrics_collector.get_metrics('example_function2')
    print(f"Function: {metrics['Function']}")
    print(f"Number of calls: {metrics['Number of calls']}")
    print(f"Average execution time: {metrics['Average execution time']} seconds")
    print(f"Number of errors: {metrics['Number of errors']}")
