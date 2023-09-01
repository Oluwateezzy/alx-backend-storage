#!/usr/bin/env python3

'''A Python module tha provides stats about nginx'''

from pymongo import MongoClient


if __name__ == '__main__':
    '''Prints the log stats in nginx collection'''
    client =  MongoClient("mongodb://localhost:27017/")
    col = client.logs.nginx

    print(f'{col.estimated_document_count()} logs')
    
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    print('Methods:')
    
    for method in methods:
        print('\tmethods {}: {}'.format(method,
              col.count_documents({'method': method})))
    print('{} status check'.format(col.count_documents(
          {'method': 'GET', 'path': '/status'})))
    pipeline = [
        {
            "$group": {"_id": "$ip", "count": {"$sum": 1}}
        },
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top = list(col.aggregate(pipeline=pipeline))
    print("IPs:")

    for idx, ip_data in enumerate(top):
        print(f"{idx + 1}. IP: {ip_data['_id']}, Count: {ip_data['count']}")

client.close()