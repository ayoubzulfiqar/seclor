import asyncio

from spider.secer import SecEdgerAsync


async def main():
    print("Running SEC Edger....")
    # APPLE INC
    await SecEdgerAsync(companyName="NFLX")


if __name__ == "__main__":
    asyncio.run(main())
# 10-K, 10-Q, 8-K, DEF 14A, F-4, S-1, SC 13D, SC 13G
# 10-K, 10-Q, 8-K, DEF 14A, F-4, S-1, SC 13D, SC 13G


# # Run multiple company searches concurrently
# async def main():
#     # More companies here
#     tasks = [
#         SecEdgerAsync("Apple Inc."),
#         SecEdgerAsync("Microsoft"),
#         SecEdgerAsync("Tesla"),
#         SecEdgerAsync("Google"),
#     ]
#     await asyncio.gather(*tasks)


# # Start the async event loop
# if __name__ == "__main__":
#     asyncio.run(main())
