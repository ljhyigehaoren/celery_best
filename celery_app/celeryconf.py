#由于celery配置信息比较多，我们可以创建一个配置文件
#http://docs.celeryproject.org/en/latest/userguide/configuration.html
#(BROKER)消息中间件
BROKER_URL = 'redis://118.24.255.219:6380/4'
#backend(存储worker执行的结果)
CELERY_RESULT_BACKEND = 'redis://118.24.255.219:6380/5'
#设置时间参照，不设置默认使用的UTC时间
CELERY_TIMEZONE = 'Asia/Shanghai'
#设置任务的序列话方式
CELERY_TASK_SERIALIZER = 'json'
#设置结果的序列化方式
CELERY_RESULT_SERIALIZER = 'json'