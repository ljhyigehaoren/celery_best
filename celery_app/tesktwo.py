from celery_app import app
import time
from celery_app.downloader import send_request
@app.task
def download2(url):
    time.sleep(5)
    html,url = send_request(url)
    return str(len(html)) + '下载完毕2'