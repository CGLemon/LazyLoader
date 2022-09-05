import random

class ShuffleBuffer:
    def __init__(self, buf_size):
        self.__buf = list()
        self.buf_size = buf_size
        assert buf_size > 4, ""

    def pop_item(self):
        if len(self.__buf) <= 0:
            return None
        return self.__buf.pop()

    def insert_item_and_pop(self, item):
        size = len(self.__buf)

        if size > 4:
            i = random.randint(0, size-1)
            self.__buf[i], item = item, self.__buf[i]

        if size < self.buf_size:
            self.__buf.append(item)
            return None
        return item
