import queue

stop = False

queue_ = queue.Queue()

while not stop:
    command = queue_.get()
    try:
        command.execute()
    except Exception:
        ...
