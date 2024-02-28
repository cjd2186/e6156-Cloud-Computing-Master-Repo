from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import Type
import uvicorn
import mysql.connector
from pydantic import BaseModel
from coaches import CoachModel, CoachResource
from assistant import AssistantModel, AssistantResource
from general import GeneralModel, GeneralResource

app = FastAPI()

# Database and table names
db_config = {
   #"host": "34.23.76.102",
   #"host": "team-mgmt-402907:us-east1:mysql-mgmt",
   "host": "team-mgmt.cx460omy2igq.us-east-1.rds.amazonaws.com",
   "database": "Managers",
   "user": "doeuser",
   "password": "doe12345",
   #"port": "3306"
}

#app.mount("/docs", StaticFiles(directory="docs", html=True), name="docs")

# Base class for resources
class BaseResource:
    def __init__(self, table_name: str, model_class: Type[BaseModel], resource_class: Type):
        self.table_name = table_name
        self.model_class = model_class
        self.resource_class = resource_class

    def get_resource_instance(self):
        return self.resource_class()

# Resources for each table
coach_resource = BaseResource("Head_Coaches", CoachModel, CoachResource)
assistant_resource = BaseResource("Assistant_Coaches", AssistantModel, AssistantResource)
general_resource = BaseResource("General_Managers", GeneralModel, GeneralResource)


# GET operations here

@app.get("/")
async def root():
    return {"message": "Dariel, microservice - Coach searching, work in progress"}

@app.get("/v1/{table_name}/{item_id}/info", response_class=HTMLResponse)
async def item_info_by_id(table_name: str, item_id: int):
    try:
        resource = None
        if table_name == "Head_Coaches":
            resource = coach_resource
        elif table_name == "Assistant_Coaches":
            resource = assistant_resource
        elif table_name == "General_Managers":
            resource = general_resource
        else:
            raise HTTPException(status_code=404, detail="Table not found")

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        query = f"SELECT * FROM {resource.table_name} WHERE id = {item_id}"

        cursor.execute(query)
        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        if len(rows) == 0:
            message = f"Sorry, no data found for {table_name} ID: {item_id}, please check the input."
            return Response(content=message, media_type="text/plain", status_code=200)
        else:
            message = "<html><body>"
            message += f"Here is the {table_name} information you requested:"
            message += "<table border='1'>"
            message += "<tr>"
            for column_name in cursor.column_names:
                message += f"<th>{column_name}</th>"
            message += "</tr>"
            for row in rows:
                message += "<tr>"
                for value in row:
                    message += f"<td>{value}</td>"
                message += "</tr>"
            message += "</table></body></html>"

        return HTMLResponse(content=message, status_code=200)

    except Exception as e:
        return Response(content=f"Error: {str(e)}", media_type="text/plain", status_code=500)

# Get paginated items for a table
@app.get("/v1/{table_name}")
async def get_paginated_items(
    table_name: str,
    limit: int = Query(default=2, le=4),
    offset: int = Query(default=0, ge=0)
):
    try:
        resource = None
        if table_name == "Head_Coaches":
            resource = coach_resource
        elif table_name == "Assistant_Coaches":
            resource = assistant_resource
        elif table_name == "General_Managers":
            resource = general_resource
        else:
            raise HTTPException(status_code=404, detail="Table not found")

        # Retrieve paginated item information
        items_data = resource.get_resource_instance().get_paginated_items(limit, offset)

        if items_data:
            # Create a list to store the result
            result_dict = {}
            data_list = []

            # Loop through the paginated item data
            for item in items_data:
                # Construct the "links" part of the response
                links = [
                    {"rel": "self", "href": f"/v1/{table_name}/{item['id']}/info"},
                    {"rel": table_name, "href": f"/v1/{table_name}"}
                ]
                item_dict = item.copy()
                item_dict["links"] = links
                data_list.append(item_dict)

            # Construct the "links" part for pagination
            prev_offset = max(offset - limit, 0)
            next_offset = offset + limit

            pagi_links = [
                {"rel": "current", "href": f"/v1/{table_name}?limit={limit}&offset={offset}"},
                {"rel": "prev", "href": f"/v1/{table_name}?limit={limit}&offset={prev_offset}"},
                {"rel": "next", "href": f"/v1/{table_name}?limit={limit}&offset={next_offset}"}
            ]

            result_dict["data"] = data_list
            result_dict["links"] = pagi_links

            return result_dict

        else:
            message = f"No {table_name} data found for the specified criteria."
            return Response(content=message, media_type="text/plain", status_code=200)

    except Exception as e:
        return Response(content=f"Error: {str(e)}", media_type="text/plain", status_code=500)

# Add a new item to a table
@app.post("/{table_name}")
async def add_item(item_data: BaseModel, table_name: str):
    try:
        resource = None
        if table_name == "Head_Coaches":
            resource = coach_resource
        elif table_name == "Assistant_Coaches":
            resource = assistant_resource
        elif table_name == "General_Managers":
            resource = general_resource
        else:
            raise HTTPException(status_code=404, detail="Table not found")

        resource.get_resource_instance().add_item(item_data)
        item_id = item_data.id
        item_name = getattr(item_data, 'name', '')

        message_content = f'New {table_name.capitalize()} {item_name} Added to the database!'
        subject = f"{table_name.capitalize()} Added"

        GET_response = await item_info_by_id(table_name, item_id)

        return GET_response

    except Exception as e:
        return Response(content=f"Error: {str(e)}", media_type="text/plain", status_code=500)

# Modify an item in a table by ID
@app.put("/{table_name}/{item_id}")
async def modify_item(item_id: int, item_data: BaseModel, table_name: str):
    try:
        resource = None
        if table_name == "Head_Coaches":
            resource = coach_resource
        elif table_name == "Assistant_Coaches":
            resource = assistant_resource
        elif table_name == "General_Managers":
            resource = general_resource
        else:
            raise HTTPException(status_code=404, detail="Table not found")

        resource.get_resource_instance().modify_item(item_id, item_data)

        GET_response = await item_info_by_id(table_name, item_id)
        return GET_response

    except Exception as e:
        return Response(content=f"Error: {str(e)}", media_type="text/plain", status_code=500)


# Delete an item from a table by ID
@app.delete("/{table_name}/{item_id}")
async def delete_item(item_id: int, table_name: str):
    try:
        resource = None
        if table_name == "Head_Coaches":
            resource = coach_resource
        elif table_name == "Assistant_Coaches":
            resource = assistant_resource
        elif table_name == "General_Managers":
            resource = general_resource
        else:
            raise HTTPException(status_code=404, detail="Table not found")

        resource.get_resource_instance().delete_item(item_id)

        message = f"Deleted {table_name.capitalize()} with ID: {item_id}."
        return Response(content=message, media_type="text/plain", status_code=200)

    except Exception as e:
        return Response(content=f"Error: {str(e)}", media_type="text/plain", status_code=500)


if __name__ == "__main__":
  #  try:
  #      connection = mysql.connector.connect(**db_config)
  #      print("Connected to MySQL")
  #  except Exception as e:
  #      print(f"Error: {str(e)}")

    #uvicorn.run(app, host="127.0.0.1", port=8000)
    uvicorn.run(app, host="0.0.0.0", port=8000)





