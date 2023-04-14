import threading
from functools import wraps

# Define the timeout decorator
def timeout(seconds=1):
    def decorator(func):
        # Define the wrapper function with a thread and timer
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Define the target function for the thread
            def target():
                # Execute the original function and save the result
                result_dict['result'] = func(*args, **kwargs)
                # Mark the function as completed
                result_dict['completed'] = True
                # Signal the event to notify completion
                event.set()

            # Create a dictionary to store the function result and completion status
            result_dict = {'result': None, 'completed': False}
            # Create an event to signal completion
            event = threading.Event()
            # Create a timer to enforce the timeout
            timer = threading.Timer(seconds, event.set)
            timer.start()

            try:
                # Create a thread to execute the target function
                target_thread = threading.Thread(target=target)
                target_thread.start()
                # Wait for the event to be set, or for the timeout to expire
                event.wait(seconds)
            except:
                # Raise any exception that occurred during execution
                raise
            finally:
                # Cancel the timer to prevent it from triggering after completion
                timer.cancel()

            # Check if the function completed within the timeout period
            if not result_dict['completed']:
                # Clear the event and raise a TimeoutError
                event.clear()
                raise TimeoutError(f"Function {func.__name__} timed out")

            # Return the function result
            return result_dict['result']
        return wrapper
    return decorator
