import asyncio
import aiohttp
import json

resources = [
    {
        "resource": "team_management",
        "url": 'https://virtserver.swaggerhub.com/bezaamsalu/NFLTeamManagement/1.0.0/teams/23871'
    },
    {
        "resource": "nfl_searching",
        "url": 'https://virtserver.swaggerhub.com/bezaamsalu/NFLSearching/1.0.0/players/14985'
    },
    {
        "resource": "projects",
        "url": 'https://virtserver.swaggerhub.com/bezaamsalu/PostSvc/1.0.0/posts/14895/1245'
    }
]

async def fetch(session, resource):
    url = resource["url"]
    print("Calling URL = ", url)
    async with session.get(url) as response:
        t = await response.json()
        print("URL ", url, "returned", str(t))
        result = {
            "resource": resource["resource"],
            "data": t
        }
    return result



async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(fetch(session, res)) for res in resources]
        responses = await asyncio.gather(*tasks)
        full_result = {}
        for response in responses:
            full_result[response["resource"]] = response["data"]

        print("\nFull Result [ASYNC] = ", json.dumps(full_result, indent=2))
    


loop = asyncio.get_event_loop()

for i in range(10):
    loop.run_until_complete(main())

