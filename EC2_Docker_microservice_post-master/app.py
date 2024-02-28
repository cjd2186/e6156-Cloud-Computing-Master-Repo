#from flask import Flask
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
import uvicorn
import mysql.connector
from resources import post

app = FastAPI()
post_resource = post.PostResource()

db_config = {
    "host": "database-post-review1.cit0asqzs92v.us-east-2.rds.amazonaws.com",
    "user": "cl4294",
    "password": "written-by-gpt4",
    "database": "cloud_computing_db",
}

# @app.get('/')
# def hello_world():
#     return 'I promise it will be a meaningful post later, but for now: Hello, World!'

"""
GET operations here
"""
@app.get("/")
async def root():
    return {"message": "From Harry Liu, Microservice - Post"}


@app.get("/posts/{user_id}/{post_id}", response_class=HTMLResponse)
async def get_post_by_ids(user_id: int, post_id: int):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = ("SELECT * FROM posts WHERE user_id = %s AND post_id = %s")
        cursor.execute(query, (user_id, post_id))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        post_id, created_time, last_edit_time, texts, user_id = result[0], result[1], result[2], result[3], result[4]
        msg = "<html><body>" + texts + "</body></html>"
        print("text: ", texts)
        return HTMLResponse(content=msg, status_code=200)
    except Exception as e:
        return Response(status_code=500, content=str(e))
    
@app.get("/posts/author/{user_id}/{post_id}", response_class=HTMLResponse)
async def get_post_author(user_id: int, post_id: int):  
    try:
        result = post_resource.get_post_author(user_id, post_id)
        return result
    except Exception as e:
        return Response(status_code=500, content=str(e))



# @app.get("/posts/{user_id}/{post_id}")
# async def get_post_by_ids(user_id: int, post_id: int):
#     try:
#         result = post_resource.get_post_by_ids(user_id, post_id)
#         return result
#     except Exception as e:
#         return Response(status_code=500, content=str(e))

@app.get("/posts/all")
async def get_all_posts(limit=100, offset=0):
    try:
        # works but not using ORM
        # connection = mysql.connector.connect(**db_config)
        # cursor = connection.cursor()
        # query = ("SELECT * FROM posts")
        # cursor.execute(query)
        # result = cursor.fetchall()
        # cursor.close()
        # connection.close()
        # return result

        result = post_resource.get_all_posts(limit, offset)
        return result
    except Exception as e:  
        return Response(status_code=500, content=str(e))

"""
POST operations here
"""

@app.post("/posts/create/{user_id}/{post_id}")
async def create_post(user_id: int, post_id: int, texts: str):
    try:
        post_resource.create_post(post_id, user_id, texts)

        GET_response = await get_post_by_ids(user_id, post_id)
        return GET_response
    except Exception as e:
        return Response(status_code=500, content=str(e))



"""
PUT operations here
"""

@app.put("/posts/edit/{user_id}/{post_id}")
async def edit_post(user_id: int, post_id: int, texts: str):
    try:
        post_resource.edit_post(user_id, post_id, texts)

        GET_response = await get_post_by_ids(user_id, post_id)
        return GET_response
    except Exception as e:
        
        return Response(status_code=500, content=str(e))
    
    #return HTMLResponse(content="Post edited successfully", status_code=200)

"""
DELETE operations here
"""

@app.delete("/posts/delete/{user_id}/{post_id}")
async def delete_post(user_id: int, post_id: int):
    try:
        post_resource.delete_post(user_id, post_id)
        return HTMLResponse(content="Post deleted successfully", status_code=200)
    except Exception as e:
        return Response(status_code=500, content=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=5001)
