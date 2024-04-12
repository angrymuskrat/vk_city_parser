from asyncio import sleep

from crawler import Crawler
import queue

from tasks import Task


class MasterCrawler:
    def __init__(self, crawler_count: int, crawler_tokens: list[str]):
        self.crawler_count = crawler_count
        self.crawler_tokens = crawler_tokens
        self.crawlers = []
        self.queue = queue.Queue()
        for i in range(crawler_count):
            self.crawlers.append(Crawler(crawler_tokens[i]))

    def add_request(self, task: Task):
        self.queue.put(task)

    def execute(self):
        while True:
            for i in range(self.crawler_count):
                match self.crawlers[i].status:
                    case "free":
                        if not self.queue.empty():
                            self.crawlers[i].status = "busy"
                            self.crawlers[i].task = self.queue.get()
                            self.crawlers[i].execute_task()
                    case "busy":
                        continue
                    case "done":
                        print(self.crawlers[i].task.result)
                        self.crawlers[i].task = None
                        self.crawlers[i].status = "free"
            sleep(100)
