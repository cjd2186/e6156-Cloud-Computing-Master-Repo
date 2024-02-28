from pydantic import BaseModel
import sqlalchemy as db_al
import os
import datetime
from dotenv import load_dotenv

load_dotenv()

# define a Pydantic data model for a post
class PostModel(BaseModel):
    post_id: int
    created_time: None
    last_edit_time: None
    texts: str
    user_id: int


# define a class for post to interact with database
class PostResource:
    def __init__(self):
        # get database info from .env file
        self.db_user = os.getenv("DB_USERNAME")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT")
        self.db_name = os.getenv("DB_NAME")
        self.db_url = f"mysql+mysqlconnector://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        self.engine = db_al.create_engine(self.db_url)
        self.connection = self.engine.connect()
        self.metadata = db_al.MetaData()
        self.posts = db_al.Table('posts', self.metadata, autoload_with=self.engine)
        self.users = db_al.Table('users', self.metadata, autoload_with=self.engine)

    def get_post_by_ids(self, user_id: int, post_id: int):
        query = db_al.select([self.posts]).where(db_al.and_(self.posts.columns.user_id == user_id, self.posts.columns.post_id == post_id))
        result = self.connection.execute(query).fetchone()
        post_id, created_time, last_edit_time, texts, user_id = result[0], result[1], result[2], result[3], result[4]
        return PostModel(post_id=post_id, created_time=created_time, last_edit_time=last_edit_time, texts=texts, user_id=user_id)

    def edit_post(self, user_id: int, post_id: int, texts: str):
        curr_time = datetime.datetime.now()
        query = db_al.update(self.posts).values(texts=texts, last_edit_time=curr_time).where(db_al.and_(self.posts.columns.user_id == user_id, self.posts.columns.post_id == post_id))
        result = self.connection.execute(query)
        self.connection.commit()
        return result

    def create_post(self, post_id: int, user_id: int, texts: str):
        # print("post_id", post_id)
        # print("user_id", user_id)
        # print("texts", texts)
        curr_time = datetime.datetime.now()
        query = db_al.insert(self.posts).values(post_id=post_id, created_time=curr_time, last_edit_time=curr_time, user_id=user_id, texts=texts)
        result = self.connection.execute(query)
        self.connection.commit()
        return result

    def delete_post(self, user_id: int, post_id: int):
        query = db_al.delete(self.posts).where(db_al.and_(self.posts.columns.user_id == user_id, self.posts.columns.post_id == post_id))
        result = self.connection.execute(query)
        self.connection.commit()
        return result

    def get_all_posts(self, limit=5, offset=1):
        #print("type", type(self.posts))
        query = db_al.select(self.posts)
        #print("posts", type(self.posts))
        # print("query", type(query))

        # apply pagination
        query = query.limit(limit).offset(offset)

        exec = self.connection.execute(query)
        result = exec.fetchall()
        #print("result", result)
        col_names = exec.keys()
        #print("col_names", col_names)
        result_dict = [dict(zip(col_names, row)) for row in result]
        return result_dict
    
    def get_post_author(self, user_id: int, post_id: int):
        #print("line 81 haha")
        query = db_al.select(self.posts).where(self.posts.columns.post_id == post_id, self.posts.columns.user_id == user_id)
        result = self.connection.execute(query).fetchone()
        #print("result", result)
        user_id = result[4]
        #print("user_id", user_id)
        query = db_al.select(self.users).where(self.users.columns.user_id == user_id)
        result = self.connection.execute(query).fetchone()
        username = result[1]
        #print("username", username)
        return username
