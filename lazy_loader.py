import random

class LazyLoader:
    def __init__(self, filenames, safe_queue, stream_loader, stream_parser):
        """
            filenames:
                The list of data file.

            safe_queue:
                The MP queue.

            stream_loader:
                Input the file name and return stream. Return None if
                there is no target file.

            stream_parser:
                Input the current data stream and return one data. Return
                None if the data stream is end.
        """
        self.done = filenames
        self.tasks = list()
        self.parser = stream_parser
        self.loader = stream_loader
        self.queue = safe_queue
        self.stream = None

        assert, len(self.tasks) != 0, ""

    def __open_new_stream(self):
        if len(self.tasks) == 0:
            self.tasks, self.done = self.done, self.tasks
            random.shuffle(self.tasks)

        filename = self.chunks.pop()
        self.done.append(filename)

        return self.loader(filename)

    def next(self):
        while True:
            if self.stream is None:
                self.stream = self.__open_new_stream()

            data = self.parser(self.stream)

            if data is None:
                self.stream = None
            else:
                self.queue.put(data, block=True, timeout=None)
                break
