import time
import functools
from django.db import connection, reset_queries
import logging


logging.basicConfig(level=logging.DEBUG)


class QueryInspectorMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        response = self.get_response(request)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        logging.debug(f"--------------------------------------------")
        logging.debug(f"Request: {request.META['PATH_INFO']}  Method: {request.META['REQUEST_METHOD']}")
        logging.debug(f"Number of Queries: {end_queries-start_queries}")
        logging.debug(f"Finished in: {(end - start):.2f}")
        logging.debug(f"--------------------------------------------")
        return response


def query_debugger(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print("Function : ", func.__name__)
        print("Number of Queries :", end_queries - start_queries)
        print("Finished in : %.2fs" % (end - start))
        return result

    return wrapper
