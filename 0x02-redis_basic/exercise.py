#!/usr/bin/env python3
"""
Main file
"""
import redis
import uuid
from typing import Union, Callable, Any
import functools


def count_calls(method: Callable) -> Callable:
    """ Count methods """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """ wrapper """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    def __init__(self) -> None:
        """ Initialize """
        self._redis = redis.Redis()
        self._redis.flushdb()
    
    def store(self, data: Union[str, bytes, int , float]) -> str:
        """ store """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
    
    def get(self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        """ get method """
        data = self._redis.get(key)
        return fn(data) if fn is not None else data
    
    def get_str(self, key: str):
        """ get string """
        return self.get(key, lambda x: x.decode('utf-8'))
    
    def get_int(self, key: str):
        """ get integer """
        return self.get(key, lambda x: int(x))
