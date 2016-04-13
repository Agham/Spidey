import threading
from queue import Queue
from spider import Spider
from general import *
from domain import *

PROJECT_NAME = input()
HOMEPAGE = input()
DOMAIN_NAME = get_domain_name(HOMEPAGE)
print('DOMAIN_NAME = '+DOMAIN_NAME)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8

#This is thread queue
queue = Queue()

Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# DO the next job in the queue
def work():
    while 1:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check for items in queue and crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links):
        print(str(len(queued_links)) + ' items remaining in the queue')
        create_jobs()

create_workers()
crawl()