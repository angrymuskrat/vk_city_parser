import threading
import uvicorn

from api.endpoints import master_crawler, app

if __name__ == "__main__":
    thread = threading.Thread(target=master_crawler.execute)
    thread.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
