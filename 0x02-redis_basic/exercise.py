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


def call_history(method: Callable) -> Callable:
    """ call history """
    @functools.wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """ wrapper function """
        inKey = '{}:imputs'.format(method.__qualname__)
        outKey = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(inKey, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(outKey, output)
        return output
    return invoker


class Cache:
    def __init__(self) -> None:
        """ Initialize """
        self._redis = redis.Redis()
        self._redis.flushdb()
    
    @call_history
    @count_calls
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
