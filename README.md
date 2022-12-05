# Lazy Loader

專們為了巨量資料而設計的資料載入器。

## Usage

首先必須先將一整個資料切割成多份並儲存在硬碟上，切割的份數盡可能多，接下來就可以用 Lazy Loader 載入之，以下是它使用的範例。

```python
from lazy_loader import LazyLoader

loader = LazyLoader(
    filenames = ['file1', 'file2', 'file3'], # 切割資料的檔案名稱
    stream_loader = stream_loader,           # 實做的載入器
    stream_parser = stream_parser,           # 實做的解析器
    batch_generator = batch_generator,       # 實做的生產器
    down_sample_rate = 16,                   # 有 1/N 的機率採樣資料，越大則資料擴散度越好
    num_workers = 4,                         # 載入器數目，越多載入速度越快
    buffer_size = 32 * 1024,                 # 緩衝大小，越大能提供越好的亂度，但需要的記憶體容量越大
    batch_size = 256                         # batch 大小
)

for _ in range(10000):
    batch = next(loader) # 可以一直拿取下一份 batch

# 程式結束可以自動釋放
```

而 ```StreamLoader``` 、```StreamParser``` 和 ```BatchGenerator``` 的實做界面為下。

```python
class StreamLoader:
    def __init__(self):
        pass

    def func(self, filename):
        
        # 輸入檔案的名稱，載入檔案轉換成 stream 並回傳之，
        # 如果檔案不存在，必須回傳 None

        return stream


class StreamParser:
    def __init__(self):
        pass

    def func(self, stream):

        # 輸入檔案的 stream ，解析 stream 內的一份資料並回傳，
        # 如果 stream 已經結束無法解析資料，必須回傳 None

        return data


class BatchGenerator:
    def __init__(self):
        pass

    def func(self, data_list):

        # 輸入是資料的 list，回傳串接好的 batch 資料

        return batch
```

## License

沒有 License ，請自由的加入自己的專案中。

## TODO

* 支援 LMDB ？
