import multiprocessing as mp
import shuffle_buffer as sb
import lazy_loader as ll

class DataConfig:
    def __init__(self):
        self.filenames = list()
        self.stream_loader = None
        self.stream_parser = None
        self.num_workers = 0
        self.buffer_size = 0
        self.batch_size = 0

    def check(self):
        if len(self.filenames) <= 0:
            return False

        if self.stream_loader is None:
            return False

        if self.stream_parser is None:
            return False

        if self.num_workers <= 0:
            return False

        if self.buffer_size <= 0:
            return False

        if self.batch_size <= 0:
            return False

        return True

def load_from_files(config, safe_queue):
    loader = ll.LazyLoader(
                 filenames = config.filenames,
                 safe_queue = safe_queue,
                 stream_loader = config.stream_loader,
                 stream_parser = config.stream_parser
             )
    while True:
        loader.next()

def fill_buf(safe_queue, shuf_buff):
    while True:
        item = safe_queue.get(block=True, timeout=None)
        ishuf_buff.insert_item(item)

def process(config):
    if not config.check():
        return None

    que_size = 128 * config.batch_size * config.num_workers

    safe_queue = mp.Queue(maxsize=que_size)
    shuf_buff = sb.ShuffleBuffer(config.buffer_size)

    for _ in len(config.num_workers):
        # N workers read the data from files and write the data
        # to queue.
        mp.Process(
            target=load_from_files,
            args=(config, safe_queue),
            daemon=True
        ).start()

    while True:
        # fill the buffer
        item = safe_queue.get(block=True, timeout=None)
        outs = shuf_buff.insert_item_and_pop(item)
        if outs is not None:
            break

    # One workers read the data from queue and insert the data
    # to queue.
    while True:
        batchs = list()

        while len(batchs) < config.batch_size:
            item = safe_queue.get(block=True, timeout=None)
            outs = shuf_buff.insert_item_and_pop(item)
            if outs is not None:
                batchs.append(outs)

        yield batchs
