import _thread
import sys
import threading


def quit_function():
    sys.stderr.flush()  # Python 3 stderr is likely buffered.
    _thread.interrupt_main()  # raises KeyboardInterrupt


def exit_after(seconds):
    """
    Use as decorator to exit process if
    function takes longer than s seconds
    """
    def outer(fn):
        def inner(*args, **kwargs):
            timer = threading.Timer(seconds, quit_function)
            timer.start()
            try:
                result = fn(*args, **kwargs)
            finally:
                timer.cancel()
            return result
        return inner
    return outer
