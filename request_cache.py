import requests
import redis


def smart_cache(func):
    def wrapped(request_cache, url, parameters, *args):
        key = get_cache_key(parameters, url)
        stored_json = request_cache.redis_cache.get(key)

        if stored_json is None:
            json_value = func(request_cache, url, parameters, *args)
            request_cache.redis_cache.set(key, json_value)
        else:
            json_value = stored_json
        return json_value
    return wrapped


def invalidate_cache(func):
    def wrapped(request_cache, url, parameters, *args):
        key = get_cache_key(parameters, url)
        request_cache.redis_cache.set(key, None)

        return func(request_cache, url, parameters, *args)
    return wrapped


def get_cache_key(parameters, url):
    parameters_str = ""
    for key in parameters:
        parameters_str += (key + ";" + str(parameters[key])) + ";"
    return url + ";" + parameters_str


class RequestCache:

    def __init__(self):
        self.redis_cache = redis.Redis(host='localhost', port=6379, db=0)

    @smart_cache
    def get(self, url, parameters=None):
        return requests.get(url, params=parameters).json()

    @invalidate_cache
    def post(self, url, parameters=None, data=None):
        return requests.post(url, params=parameters, data=data).json()

    @invalidate_cache
    def put(self, url, parameters=None, data=None):
        return requests.put(url, params=parameters, data=data).json()

    @invalidate_cache
    def patch(self, url, parameters=None, data=None):
        return requests.patch(url, params=parameters, data=data).json()

    @invalidate_cache
    def delete(self, url, parameters=None, data=None):
        return requests.delete(url, params=parameters, data=data).json()
