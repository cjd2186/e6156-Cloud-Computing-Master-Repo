import json
import requests

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

def fetch_sync(resource):
    url = resource["url"]
    print("Calling URL = ", url)
    response = requests.get(url)
    t = response.json()
    print("URL ", url, "returned", str(t))
    result = {
        "resource": resource["resource"],
        "data": t
    }
    return result

def main_sync():
    full_result = {}
    for res in resources:
        response = fetch_sync(res)
        full_result[response["resource"]] = response["data"]

    print("\n\nFull Result [SYNC]= ", json.dumps(full_result, indent=2))

main_sync()