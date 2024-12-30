import threading
from queue import Queue
import time

class ThreadedProcessor:
    def __init__(self, callback=None):
        self.callback = callback
        self.queue = Queue()
        self.is_processing = False
        self.current_thread = None
        self.cancelled = False
    
    def process(self, func, *args, **kwargs):
        """Start processing in a separate thread"""
        self.is_processing = True
        self.cancelled = False
        self.current_thread = threading.Thread(
            target=self._process_wrapper,
            args=(func, args, kwargs)
        )
        self.current_thread.daemon = True
        self.current_thread.start()
        return self.current_thread
    
    def cancel(self):
        """Cancel the current processing"""
        self.cancelled = True
        if self.current_thread and self.current_thread.is_alive():
            self.is_processing = False
    
    def _process_wrapper(self, func, args, kwargs):
        """Wrapper to handle the processing and callback"""
        try:
            if not self.cancelled:
                result = func(*args, **kwargs)
                if self.callback and not self.cancelled:
                    self.queue.put((True, result))
        except Exception as e:
            if self.callback and not self.cancelled:
                self.queue.put((False, str(e)))
        finally:
            self.is_processing = False
    
    def update(self):
        """Check for completed processing and trigger callback"""
        if not self.queue.empty():
            success, result = self.queue.get()
            if self.callback:
                self.callback(success, result)
            return True
        return False