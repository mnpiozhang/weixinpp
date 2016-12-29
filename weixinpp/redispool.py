import redis
import config as cf

pool = redis.ConnectionPool(host=cf.REDIS_SERVER, port=cf.REDIS_PORT, db=0)
