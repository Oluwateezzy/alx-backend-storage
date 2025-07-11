#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests


redis_store = redis.Redis()
'''The module-level Redis instance.
'''

count = 0


def get_page(url: str) -> str:
    """get a page and cach value"""
    redis_store.set(f"cached:{url}", count)
    resp = requests.get(url)
    redis_store.incr(f"count:{url}")
    redis_store.setex(f"cached:{url}", 10, redis_store.get(f"cached:{url}"))
    return resp.text
