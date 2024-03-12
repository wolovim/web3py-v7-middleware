import os
from web3 import AsyncWeb3, AsyncHTTPProvider
from web3.middleware.base import Web3Middleware
from dotenv import load_dotenv
import asyncio

# load env vars
load_dotenv()

RPC_URL = os.getenv("RPC_URL")


# define custom middleware
class CustomAsyncMiddleware(Web3Middleware):
    async def async_request_processor(self, method, params):
        print(f"∆∆∆ custom: pre-request {method}")
        return (method, params)

    async def async_response_processor(self, method, response):
        print(f"∆∆∆ custom: post-response {method}")
        return response


class CustomWrapAsyncMiddleware(Web3Middleware):
    async def async_wrap_make_request(self, make_request):
        async def middleware(method, params):
            print(f"∆∆∆ custom wrap: pre-request {method}")
            response = await make_request(method, params)
            print(f"∆∆∆ custom wrap: post-request {method}")
            return response

        return middleware


w3 = AsyncWeb3(AsyncHTTPProvider(RPC_URL))
print(f"web3.py version: ${w3.api}")

w3.middleware_onion.add(CustomAsyncMiddleware, name="custom_async_middleware")
w3.middleware_onion.add(CustomWrapAsyncMiddleware, name="custom_wrap_async_middleware")

print("∆∆∆ middleware onion:")
print([m[1] for m in w3.middleware_onion.middleware])


async def main():
    print("∆∆∆ starting get_block...")
    await w3.eth.get_block("latest")
    print("∆∆∆ ...finished get_block")


asyncio.run(main())

"""
Sample command line output:

❯ python async.py
web3.py version: $7.0.0b1
middleware onion:
['custom_wrap_async_middleware', 'custom_async_middleware', 'gas_price_strategy', 'ens_name_to_address', 'attrdict', 'validation', 'gas_estimate']
∆∆∆ starting get_block...
∆∆∆ custom wrap: pre-request eth_getBlockByNumber
∆∆∆ custom: pre-request eth_getBlockByNumber
∆∆∆ custom: post-response eth_getBlockByNumber
∆∆∆ custom wrap: post-request eth_getBlockByNumber
∆∆∆ ...finished get_block
"""
