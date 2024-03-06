import os
from web3 import Web3, HTTPProvider
from web3.middleware.base import Web3Middleware
from dotenv import load_dotenv

# load env vars
load_dotenv()

RPC_URL = os.getenv("RPC_URL")


# define custom middleware
class CustomMiddleware(Web3Middleware):
    def request_processor(self, method, params):
        print(f"∆∆∆ custom: pre-request {method}")
        return (method, params)

    def response_processor(self, method, response):
        print(f"∆∆∆ custom: post-response {method}")
        return response


class CustomWrapMiddleware(Web3Middleware):
    def wrap_make_request(self, make_request):
        def middleware(method, params):
            print("∆∆∆ custom wrap: pre-request")
            response = make_request(method, params)  # make the request
            print("∆∆∆ custom wrap: post-request")
            return response

        return middleware


w3 = Web3(HTTPProvider(RPC_URL))
print(f"web3.py version: ${w3.api}")

w3.middleware_onion.add(CustomMiddleware, name="custom_middleware")
w3.middleware_onion.add(CustomWrapMiddleware, name="custom_wrap_middleware")

print("∆∆∆ middleware onion:")
print([m[1] for m in w3.middleware_onion.middlewares])

print("∆∆∆ starting get_block...")
w3.eth.get_block("latest")
print("∆∆∆ ...finished get_block")

"""
Sample command line output:

❯ python sync.py
web3.py version: $7.0.0b1
middleware onion:
['custom_wrap_middleware', 'custom_middleware', 'gas_price_strategy', 'ens_name_to_address', 'attrdict', 'validation', 'gas_estimate']
∆∆∆ starting get_block...
∆∆∆ custom wrap: pre-request
∆∆∆ custom: pre-request eth_getBlockByNumber
∆∆∆ custom: post-response eth_getBlockByNumber
∆∆∆ custom wrap: post-request
∆∆∆ ...finished get_block
"""
