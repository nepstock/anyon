from queue import Queue


class Store:
    __slots__ = (
        "_check_fn",
        "_shared_queue",
    )

    def __init__(self, check_fn=None):
        self._check_fn = check_fn
        self._shared_queue = Queue()

    def put(self, item):
        self._shared_queue.put(item)

    def get(self, **kwargs):
        if not self._shared_queue.empty():
            for item in list(self._shared_queue.queue):
                if self._check_fn and self._check_fn(item, **kwargs):
                    return item
        return None
