#!/usr/bin/env python3
""" 101-main """

def top_students(mongo_collection):
    """Mongo database"""
    pipeline = [
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ]
    return list(mongo_collection.aggregate(pipeline))