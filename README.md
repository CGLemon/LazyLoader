# Lazy Loader

專們為了巨量資料而設計的資料載入器。

## Usage

首先必須先將一整個資料切割成多份並儲存在硬碟上，切割的份數盡可能多，接下來就可以用 Lazy Loader 載入之，以下是它使用的範例。

```python
from lazy_loader import LazyLoader

loader = LazyLoader(
    filenames = ['file1', 'file2', 'file3'], # 切割的檔案名稱
    stream_loader = stream_loader,
    stream_parser = stream_parser,
    batch_generator = batch_generator,
    down_sample_rate = 16,
    num_workers = 4,
    buffer_size = 32 * 1024, # 緩衝大小，越大能提供越好的亂度
    batch_size = 256
)

for _ in range(10000):
    batch = next(loader) # infinite loader # 可以一直拿取下一份 batch
```

而 ```StreamLoader``` 、 ```StreamParser``` 和 ```BatchGenerator``` 的間單實做為。

```python
class StreamLoader:
    def __init__(self):
        pass

    def func(self, filename):
        
        # 輸入檔案的名稱，載入檔案並回傳 stream

        return stream


class StreamParser:
    def __init__(self):
        pass

    def func(self, stream):

        # 輸入檔案的 stream ，回傳 stream 內的一份資料，
        # 如果 stream 已經尾，則回傳 None

        return data


class BatchGenerator:
    def __init__(self):
        pass

    def func(self, data_list):

        # 輸入資料的 list，回傳串接好的 batch 資料

        return batch
```

你也可以到 ```test.py``` 看實際實做和應用方法。
