import os, random, glob, io
from lazy_loader import LazyLoader

def gen_dummy_data():
    dirname = "dummy-data"
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

    print("write the sample data in the {} file...\n".format(dirname))

    for i in range(10):
        filename = os.path.join(dirname, "data_{}.txt".format(i+1))
        if not os.path.isfile(filename):
            with open(filename, 'w') as f:
                for j in range(1024):
                    random_list = list()
                    for k in range(2):
                        random_list.append(random.randint(0, 99999))
                    for r in random_list:
                        f.write("{} ".format(r))
                    f.write("\n")

def gather_filenames():
    def gather_recursive_files(root):
        l = list()
        for name in glob.glob(os.path.join(root, "*")):
            if os.path.isdir(name):
                l.extend(gather_recursive_files(name))
            else:
                l.append(name)
        return l

    return gather_recursive_files("dummy-data")

class StreamLoader:
    def __init__(self):
        pass

    def func(self, filename):
        stream = None
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                stream = io.StringIO(f.read())
        return stream

class StreamParser:
    def __init__(self):
        pass

    def func(self, stream):
        if stream is None:
            return None

        line = stream.readline()
        if len(line) == 0:
            return None

        data = list()
        vals = line.split()
        for v in vals:
           data.append(int(v))
        return data

class BatchGenerator:
    def __init__(self):
        pass

    def func(self, data_list):
        x = list()
        y = list()

        for data in data_list:
            x.append(data[0])
            y.append(data[1])

        batch = x, y
        return batch

if __name__ == "__main__":
    # Create sample data.
    gen_dummy_data()

    # Implement the loader, parser and generator.
    sl = StreamLoader()
    sp = StreamParser()
    bg = BatchGenerator()

    # Create the lazy loader.
    loader = LazyLoader(
        filenames = gather_filenames(),
        stream_loader = sl,
        stream_parser = sp,
        batch_generator = bg,
        down_sample_rate = 16,
        num_workers = 1,
        buffer_size = 512,
        batch_size = 32
    )

    # Wait for filling shuffle buffer. 
    batch = next(loader)

    # gather batch
    for _ in range(10):
        batch = next(loader)
        print(batch)
