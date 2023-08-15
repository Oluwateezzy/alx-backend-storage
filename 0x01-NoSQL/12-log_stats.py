#!/usr/bin/env python3
'''A Python module tha provides stats about nginx'''

from pymongo import MongoClient
if __name__ == '__main__':
    '''Prints the log stats in nginx collection'''
    client =  MongoClient("mongodb://localhost:27017/")
    col = client.logs.nginx
    print(f'{col.estimated_document_count()} logs')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        print('\tmethods {}: {}'.format(method,
              col.count_documents({'method': method})))
    print('{} status check'.format(col.count_documents(
          {'method': 'GET', 'path': '/status'})))
    client.close()