from functools import wraps
import threading

def timeout(seconds=1):
    """
    A decorator that adds a timeout to a function call.

    Args:
        seconds (float): The number of seconds before the function call times out.

    Returns:
        function: The decorated function with a timeout.

    Raises:
        TimeoutError: If the function call takes longer than the specified number of seconds.

    Example:
        >>> @timeout(1.0)
        ... def my_function():
        ...     time.sleep(2.0)
        ...
        ... my_function()
        TimeoutError: Function my_function timed out
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            def target():
                """
                A target function that calls the wrapped function and sets a flag when it completes.
                """
                nonlocal result, completed
                result = func(*args, **kwargs)
                completed = True

            # Initialize variables
            completed = False
            result = None

            # Create a timer object to trigger the timeout
            timer = threading.Timer(seconds, lambda: None)
            timer.start()

            try:
                # Create a new thread to call the target function
                target_thread = threading.Thread(target=target)
                target_thread.start()

                # Wait for the target function to complete or for the timeout to trigger
                target_thread.join(seconds)

            except:
                # Reraise any exceptions
                raise

            finally:
                # Cancel the timer to prevent it from triggering
                timer.cancel()

            # Check whether the target function completed successfully
            if not completed:
                # If not, cancel the target thread and raise a TimeoutError
                target_thread.cancel()
                raise TimeoutError(f"Function {func.__name__} timed out")

            # Return the result of the target function
            return result

        return wrapper

    return decorator