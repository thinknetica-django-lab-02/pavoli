from django.test import TestCase
import redis

# Create your tests here.
r = redis.Redis(host='localhost', port=6379, db=0)
print(r)
