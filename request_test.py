import unittest
from request_cache import RequestCache
from unittest.mock import patch


class RequestTest(unittest.TestCase):
    URL = "http://localhost"
    PARAMETERS = []
    DATA = [{'key1': 'value1'}]
    REDIS_CONTENTS = [{'key1': 'value1'}]
    RESPONSE_CONTENTS = [{'key1': 'value1'}]

    class RedisMock:

        def get(self, key):
            return RequestTest.REDIS_CONTENTS

        def set(self, key, value):
            pass

    class RedisMockEmpty:

        def get(self, key):
            return None

        def set(self, key, value):
            pass

    class ResponseMock:
        def json(self):
            return RequestTest.RESPONSE_CONTENTS

    @patch('requests.get', return_value=ResponseMock())
    @patch('redis.Redis', return_value=RedisMockEmpty())
    def test_get_previously_uncached(self, redis_mock, response_mock):
        self.requestCache = RequestCache()
        self.assertEqual(self.requestCache.get(RequestTest.URL, RequestTest.PARAMETERS), RequestTest.REDIS_CONTENTS)

        redis_mock.assert_called_once()
        response_mock.assert_called_once()

    @patch('requests.get', return_value=ResponseMock())
    @patch('redis.Redis', return_value=RedisMock())
    def test_get_already_cached(self, redis_mock, response_mock):
        self.requestCache = RequestCache()
        self.assertEqual(self.requestCache.get(RequestTest.URL, RequestTest.PARAMETERS), RequestTest.REDIS_CONTENTS)

        redis_mock.assert_called_once()
        response_mock.assert_not_called()

    @patch('requests.post', return_value=ResponseMock())
    @patch('redis.Redis', return_value=RedisMock())
    def test_post(self, redis_mock, response_mock):
        self.requestCache = RequestCache()
        self.assertEqual(self.requestCache.post(RequestTest.URL, RequestTest.PARAMETERS, RequestTest.DATA),
                         RequestTest.RESPONSE_CONTENTS)

        redis_mock.assert_called_once()
        response_mock.assert_called_once()


if __name__ == '__main__':
    unittest.main()
