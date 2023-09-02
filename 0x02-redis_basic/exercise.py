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


def replay(fn: Callable) -> None:
    """Displays the call history of a Cache class' method.
    """
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    in_key = '{}:inputs'.format(fxn_name)
    out_key = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))


def call_history(method: Callable) -> Callable:
    """ call history """
    @functools.wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """ wrapper function """
        inKey = '{}:inputs'.format(method.__qualname__)
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
