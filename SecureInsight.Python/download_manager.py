import os
import sys
import asyncio
import aiohttp
import aioconsole

urls = [
    "https://storage.googleapis.com/openimages/2016_08/human_ann_2016_08_v3.tar.gz",
    "https://storage.googleapis.com/cvdf-datasets/oid/open-images-dataset-train0.tsv",
    "https://storage.googleapis.com/cvdf-datasets/oid/open-images-dataset-train1.tsv",
    "https://storage.googleapis.com/cvdf-datasets/oid/open-images-dataset-train2.tsv",
    "https://storage.googleapis.com/cvdf-datasets/oid/open-images-dataset-train3.tsv",
    "https://storage.googleapis.com/cvdf-datasets/oid/open-images-dataset-train4.tsv",
    "https://storage.googleapis.com/cvdf-datasets/oid/open-images-dataset-train5.tsv",
    "https://storage.googleapis.com/cvdf-datasets/oid/open-images-dataset-train6.tsv",
    "https://storage.googleapis.com/cvdf-datasets/oid/open-images-dataset-train7.tsv",
    "https://storage.googleapis.com/cvdf-datasets/oid/open-images-dataset-train8.tsv",
    "https://storage.googleapis.com/cvdf-datasets/oid/open-images-dataset-train9.tsv"
]

class DownloadManager:
    def __init__(self, urls, concurrent_downloads):
        self.urls = urls
        self.concurrent_downloads = concurrent_downloads
        self.queue = asyncio.Queue()
        self.tasks = []
        self.session = None
        self.running = False
        self.pause_event = asyncio.Event()
        self.pause_event.set()
        print("DownloadManager initialized")

    async def download_file(self, url):
        print(f"Starting download: {url}")
        async with self.session.get(url) as response:
            filename = os.path.basename(url)
            with open(filename, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
            print(f"Downloaded {filename}")

    async def worker(self):
        print("Worker started")
        while self.running:
            await self.pause_event.wait()
            try:
                url = await self.queue.get()
                if url is None:
                    break
                await self.download_file(url)
                self.queue.task_done()
            except Exception as e:
                print(f"Error downloading {url}: {e}")
        print("Worker finished")

    async def start_downloads(self):
        print("Starting downloads...")
        try:
            self.session = aiohttp.ClientSession()
            for url in self.urls:
                await self.queue.put(url)
            print(f"Queue size: {self.queue.qsize()}")
            self.tasks = [asyncio.create_task(self.worker()) for _ in range(self.concurrent_downloads)]
            await self.queue.join()
            print("All tasks completed")
        except Exception as e:
            print(f"Error in start_downloads: {e}")
        finally:
            if self.session:
                await self.session.close()
            self.running = False
            print("Finished all downloads.")

    def start(self):
        if not self.running:
            self.running = True
            print("Scheduling start_downloads task")
            task = asyncio.create_task(self.start_downloads())
            task.add_done_callback(lambda t: print(f"start_downloads task done: {t}"))
            print("Started downloading")
        self.pause_event.set()

    def pause(self):
        self.pause_event.clear()
        print("Paused downloading")

    def stop(self):
        self.running = False
        self.pause_event.set()
        for _ in range(self.concurrent_downloads):
            self.queue.put_nowait(None)
        for task in self.tasks:
            task.cancel()
        self.tasks = []
        print("Stopped downloading")

async def main():
    concurrent_downloads = int(await aioconsole.ainput("Enter the number of concurrent downloads: "))
    manager = DownloadManager(urls, concurrent_downloads)
    
    while True:
        command = (await aioconsole.ainput("Enter command (start/s/1, pause/p/2, resume/r/3, stop/x/4): ")).strip().lower()
        if command in {"start", "s", "1"}:
            manager.start()
        elif command in {"pause", "p", "2"}:
            manager.pause()
        elif command in {"resume", "r", "3"}:
            manager.start()
        elif command in {"stop", "x", "4"}:
            manager.stop()
            break

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Download process interrupted")

