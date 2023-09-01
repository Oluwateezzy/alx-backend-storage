#!/usr/bin/env python3
"""
Main file
"""
import redis


class Cache:
    def __init__(self) -> None:
        """ Initialize """
        self._redit = redis.Redis()
        self._redit.flushdb()
    
    def store(data: str | bytes | int | float) -> str:
        """ store """
        
        