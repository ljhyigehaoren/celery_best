from celery_app import app
import time
from celery_app.downloader import send_request
@app.task
def download1(url):
    html,url = send_request(url)
    return str(len(html))+'下载完毕1'