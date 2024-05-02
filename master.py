from time import sleep

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
            self.crawlers.append(Crawler(i, crawler_tokens[i]))

    def add_request(self, task: Task):
        self.queue.put(task)

    def execute(self):
        while True:
            for i in range(self.crawler_count):
                print(self.crawlers[i].status)
                match self.crawlers[i].status:
                    case "free":
                        if not self.queue.empty():
                            self.crawlers[i].status = "busy"
                            self.crawlers[i].task = self.queue.get()
                    case "busy":
                        continue
                    case "done":
                        print("result for: ", self.crawlers[i].task.prompt)
                        # for result in self.crawlers[i].task.result:
                        #     print(result)
                        # print(self.crawlers[i].task.result)
                        print("-----------------------------------")
                        self.crawlers[i].task = None
                        self.crawlers[i].status = "free"
            print("----")
            sleep(1)
