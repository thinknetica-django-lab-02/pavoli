from django.test import TestCase

from django_redis import get_redis_connection


# Use the name you have defined for Redis in settings.CACHES
r = get_redis_connection("default")
connection_pool = r.connection_pool

print("Created connections so far: %d" % connection_pool._created_connections)
