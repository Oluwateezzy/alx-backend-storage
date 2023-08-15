#!/usr/bin/env python3
""" 11-main """

def schools_by_topic(mongo_collection, topic):
    """Mongo database"""
    return list(mongo_collection.find({"topics": topic}))
