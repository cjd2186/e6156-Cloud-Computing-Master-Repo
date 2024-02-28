# import libraries here
from fastapi import FastAPI, Response, Query, Request
from fastapi.responses import HTMLResponse
import uvicorn
import mysql.connector
import requests
import os
#new
import boto3
from resources import player
from dotenv import load_dotenv

import graphene
from starlette.graphql import GraphQLApp
from resources.query import TeamQuery


load_dotenv()

# instances initialization
app = FastAPI()
player_resource = player.PlayerResource()

# https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
# define MySQL connection parameters
db_config = {
    "host": "c6156-nfl-searching-query-microservice-db.ckoq7q2zprcp.us-east-2.rds.amazonaws.com",
    "user": "tw6156",
    "password": "linguine_falafel_pita",
    "database": "dbNFLstat",
}


# graphQL related
# https://www.tutorialspoint.com/fastapi/fastapi_using_graphql.html
app.add_route("/team/graphql", GraphQLApp(schema=graphene.Schema(query=TeamQuery)))

# Middleware: Logging incoming requests and outgoing response (use middleware of )
@app.middleware("http")
async def log_request_and_response_details(request: Request, call_next):
    method_name = request.method
    path = request.url.path

    # Log incoming request details
    with open("log.txt", mode="a") as log:
        content = f"Incoming Request - Method: {method_name}, Path: {path}, Received at: {datetime.now()}\n"
        log.write(content)

    # Process the request
    response = await call_next(request)

    # Log outgoing response details
    with open("log.txt", mode="a") as log:
        content = f"Outgoing Response - Method: {method_name}, Path: {path}, Status Code: {response.status_code}, Sent at: {datetime.now()}\n"
        log.write(content)

    return response

API_KEY = os.getenv("ADMIN_KEY")

# Second Middleware: API key authentication; adds a new persona
@app.middleware("http")
async def api_key_authentication(request: Request, call_next):
    api_key = request.headers.get("X-Api-Key")
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")

    response = await call_next(request)
    return response

"""
GET operations here
"""

@app.get("/")
async def root():
    return {"message": "From Tangwen Zhu (tz2570), microservice - NFL searching, work in progress"}

"""
show the player game stats information based on the player_id, and other optional information: week, and (season) year
as an html table webpage (if the connnection to the database is fine and the data can be found)
https://fastapi.tiangolo.com/advanced/custom-response/#return-an-htmlresponse-directly
"""
@app.get("/v1/players/{player_id}/stat", response_class = HTMLResponse)
async def player_stat_by_id(player_id: str, week: int=None, season: int=None):

    try:
        # connect to the MySQL server
        connection = mysql.connector.connect(**db_config)
        # create a cousor object for query
        # https://www.geeksforgeeks.org/python-sqlite-cursor-object/#
        cursor = connection.cursor()

        # define sql query here
        query = f"SELECT * FROM player_stat WHERE player_id = '{player_id}'"

        # if the year and week parameter are valid
        if week != None:
            query += f" AND week = '{week}'"

        if season != None:
            query += f" AND season = '{season}'"

        # execute query
        cursor.execute(query)

        # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-fetchall.html
        rows = cursor.fetchall() # get the result rows

        # shut down cursor and connection
        cursor.close()
        connection.close()

        # process the rows for the webpage result presentation

        # case 1 -  the player stat data doesn't exist:
        if len(rows) == 0:
            message = f"Sorry, no data found for this player under player_id : {player_id}, under week: '{week}', and season: '{season}', please check the inputs"
            return Response(content=message, media_type="text/plain", status_code=200)

        # case 2 - the player stat data exists
        else:
            # construct an HTML table
            message = "<html><body>"
            message += "Here is the performance data you requested:"
            message += "<table border='1'>"

            # header row
            message += "<tr>"
            for column_name in cursor.column_names:
                message += f"<th>{column_name}</th>"
            message += "</tr>"

            # data rows
            for row in rows:
                message += "<tr>"
                for value in row:
                    message += f"<td>{value}</td>"
                message += "</tr>"
            message += "</table></body></html>"

        return HTMLResponse(content=message, status_code=200)

    # connection error
    except Exception as e:
        return Response(content=f"Error: {str(e)}", media_type="text/plain", status_code=500)

"""
2nd version of player stat getter, using SQLalchemy
set limit to be 2 by default, maximum limit 4
set offset to be 0 by default, has to be at least 0
https://fastapi.tiangolo.com/tutorial/query-params-str-validations/
https://stackoverflow.com/questions/72217828/fastapi-how-to-get-raw-url-path-from-request
"""
@app.get("/players/{player_id}/stat")
async def player_stat_by_id2(player_id: str, request: Request, week: int=None, season: int=None,
                             limit: int = Query(default=2, le=4), offset: int = Query(default=0, ge=0)):
    try:
        
        # retrieve player stats with pagination
        player_stats_dict = player_resource.get_player_stats(player_id, week, season, limit, offset)

        # check if player stats exist
        if player_stats_dict:

            curr_url = str(request.url)
            player_url = curr_url.split("/stat")[0]

            # create a list to store the result
            result_dict = {}
            data_list = []

            # loop through the paginated player stats
            for stats in player_stats_dict:
                # construct the "links" part of the response that is to be added to the data_list
                # ask prof
                # https://stackoverflow.com/questions/70477787/how-to-get-current-path-in-fastapi-with-domain
                links = [
                    {"rel": "self", "href": curr_url},
                    {"rel": "player basics", "href": f"{player_url}"}
                ]
                stat_dict = stats.copy()
                stat_dict["links"] = links
                data_list.append(stat_dict)

            # construct the "links" part for pagination
            prev = curr_url.split("offset=")[0] + "offset=" + str(max(offset - limit, 0))
            next = curr_url.split("offset=")[0] + "offset=" + str(offset+limit)

            pagi_links = [
                {"rel": "current", "href": curr_url},
                {"rel": "prev", "href": prev},
                {"rel": "next", "href": next}
            ]

            result_dict["data"] = data_list
            result_dict["links"] = pagi_links

            return [result_dict]

        else:
            rsp = Response(
                content=f"Sorry, the player stats under player ID: {player_id} , week: {week} , season: {season}, limit: {limit}, offset: {offset} aren't in the database.",
                media_type="text/plain"
            )
            return rsp

    except Exception as e:
        # handle other exceptions if encountered
        return Response(content=f"Error: {str(e)}", media_type="text/plain", status_code=500)

"""
Show the basic information of a player by the player_id
"""
@app.get("/players/{player_id}", response_class = HTMLResponse)
async def player_by_id(player_id: str):
    try:
        player = player_resource.get_player_by_id(player_id)

        # the player is found in the table
        if player:
            player = list(player[0])
            # print(player) # debugging purpose
            message = "<html><body>"
            message += "Here is the player basic information you requested:"

            columns_name = list(player_resource.player_basic.columns.keys())
            # print(columns_name) # debugging purpose

            player_zip = zip(columns_name, player)
            for tup in player_zip:
                message += f"<h3>{tup[0]}:</h3> {tup[1]}"

            message += "</html></body>"

            rsp = Response(content=message)
            return rsp

        else:
            rsp = Response(content="Sorry, the player you are looking for is not in the database.", media_type="text/plain")
            return rsp

    except Exception as e:
        # other exceptions if encounterd
        return Response(content=f"Error: {str(e)}", media_type="text/plain", status_code=500)

#external_api_call
@app.get("/players/{player_id}/news", response_class=HTMLResponse)
async def get_news_by_id(player_id: str):
    api_key = os.getenv("API_KEY")
    url = f"https://api.sportsdata.io/v3/nfl/scores/json/NewsByPlayerID/{player_id}?key={api_key}"

    try:
        rsp = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if rsp.status_code == 200:
            # Return the content of the response
            return HTMLResponse(content=rsp.text, status_code=200)
        else:
            return Response(content="Sorry, the player you are looking for is not in the database.", media_type="text/plain", status_code=rsp.status_code)

    except requests.exceptions.RequestException as e:
        # Create a FastAPI response object with an error message
        return Response(content=f"Error: {str(e)}", media_type="text/plain", status_code=500)



"""
add a new player to the player_basic table on database, make use of the player base model in resource
"""
@app.post("/players")
async def add_player(player: player.PlayerModel):
    try:
        # add player to the database
        result = player_resource.add_player(player)
        player_id = player.player_id
        
        #new
        player_name=player.name

        sns_topic_arn = os.getenv("ARN")
        message_content = f'New Player {player_name} Added to the database!'
        subject= 'Player Added!'
        
        response= publish_to_sns_topic(sns_topic_arn, message_content, subject)
        print("Message published. Response:", response)
        
        #new end
        
        # check if the player was successfully added by showing the basic info page
        # https://fastapi.tiangolo.com/async/
        GET_response = await player_by_id(player_id)
        
        
        return GET_response

    except Exception as e:
        # other exception if encountered
        return Response(content=f"Error: {str(e)}", media_type="text/plain", status_code=500)



"""
a function to modify a player basic information from the player_basic table by player_id
"""
@app.put("/players/modify/{player_id}")
async def modify_player(player: player.PlayerModel, player_id):
    try:
        # modify the data of the player
        player_resource.modify_player(player, player_id)

        # show the modified infos using the GET operation
        # https://fastapi.tiangolo.com/async/

        
        GET_response = await player_by_id(player_id)
        return GET_response

    except Exception as e:
        # other exception if encountered
        return Response(content=f"Error: {str(e)}", media_type="text/plain", status_code=500)


"""
a function to delete a player from the player_basic table by player_id
"""
@app.delete("/players")
async def delete_player(player_id: str):
    try:
        # delete a player by the id
        player_resource.delete_player(player_id)

        message = "Done."
        return Response(content=message, media_type="text/plain", status_code=200)

    except Exception as e:
        # other exception if encountered
        return Response(content=f"Error: {str(e)}", media_type="text/plain", status_code=500)

#new
def publish_to_sns_topic(topic_arn, message, subject=None):
    """
    Publish a message to an AWS SNS topic.

    Parameters:
    - topic_arn (str): The Amazon Resource Name (ARN) of the SNS topic.
    - message (str): The message you want to publish to the topic.
    - subject (str): (Optional) The subject of the message.

    Returns:
    - dict: The response from the SNS service.
    """
    # Create an SNS client
    region= os.getenv("REGION")
    access_key= os.getenv("AWS_ACCCESS_KEY_ID")
    secret_key= os.getenv("AWS_SECRET_ACCESS_KEY")
    
    sns_client = boto3.client('sns', region_name=region, 
                              aws_access_key_id=access_key, 
                              aws_secret_access_key=secret_key)

    try:
        # Publish the message to the specified topic
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject
        )
        return response
    except Exception as e:
        # Handle the exception (e.g., log the error or raise a custom exception)
        print(f"Error publishing message to SNS topic: {e}")
        raise
#new end

if __name__ == "__main__":
    # uvicorn.run(app, host="127.0.0.1", port=8000) # local machine
    uvicorn.run(app, host="0.0.0.0", port=8000) # cloud machine
