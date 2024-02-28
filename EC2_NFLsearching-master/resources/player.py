from pydantic import BaseModel
import sqlalchemy as db_al
import os
from dotenv import load_dotenv


# https://pypi.org/project/python-dotenv/
load_dotenv()


# define a Pydantic data model for a player
class PlayerModel(BaseModel):
    player_id: str
    name: str
    position: str = None
    number: int = None
    current_Team: str = None
    height: str = None
    weight: int = None
    age: int = None
    college: str = None

# class to interact with the database for player-related operations
class PlayerResource:
    # constructor
    def __init__(self):
        db_username = os.getenv("DB_USERNAME")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = str(os.getenv("DB_PORT"))
        db_name = os.getenv("DB_NAME")
        
        # following based on https://www.datacamp.com/tutorial/sqlalchemy-tutorial-examples

        # create a SQLAlchemy engine https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine
        db_url = f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
        # print(db_url) # debugging purpose
        self.engine = db_al.create_engine(db_url)

        self.conn = self.engine.connect()

        self.metadata = db_al.MetaData()  # meta data instance for extracting the metadata: structures, table infos etc

        # table object for player_basic
        self.player_basic = db_al.Table('player_basic', self.metadata, autoload_with=self.engine)

        # table object for player stat table
        self.player_stat = db_al.Table('player_stat', self.metadata, autoload_with=self.engine)

    """
    function to retrieve player information by player ID from the database
    @param player_id: the player id
    @return result: a list of tuple(s)
    """
    def get_player_by_id(self, player_id):
        query = self.player_basic.select().where(self.player_basic.columns.player_id == player_id)
        exe = self.conn.execute(query)  # executing the query
        result = exe.fetchall()
        return result

    """
       function to retrieve player stat information by player ID from the database
       @param player_id: the player id
       @param week: the week of the year (season)
       @param season: the season -- year
       @param limit: item per page
       @param offset: offset
       @return result_dicts: dictionaries in a list that looks like this: [{'event_id': 1, 'player_id': '1', 'name': 'A.J. Brown', 'position': 'WR'...}] 
       """
    def get_player_stats(self, player_id, week: int=None, season: int=None,
                         limit: int=2, offset: int=0):
        # the initial select query
        query = self.player_stat.select().where(self.player_stat.columns.player_id == player_id)

        # add optional filters for week and season if provided
        if week is not None:
            query = query.where(self.player_stat.columns.week == week)

        if season is not None:
            query = query.where(self.player_stat.columns.season == season)

        # apply pagination
        # https://stackoverflow.com/questions/20642497/sqlalchemy-query-to-return-only-n-results
        query = query.limit(limit).offset(offset)

        # execute
        exe = self.conn.execute(query)
        result = exe.fetchall()

        # get column names
        # https://stackoverflow.com/questions/20743806/sqlalchemy-execute-return-resultproxy-as-tuple-not-dict
        column_names = exe.keys()

        # convert each row to a dictionary
        result_dicts = [dict(zip(column_names, row)) for row in result]

        return result_dicts
    
    """
    function to add player using PlayerModel to the player_basic table
    @param player: the PlayerModel representation of a new player
    @return result: the Cursor result
    """
    def add_player(self, player: PlayerModel):
        # the insertion query
        ins_query = self.player_basic.insert().values(
            player_id=player.player_id,
            name=player.name,
            position=player.position,
            number=player.number,
            current_Team=player.current_Team,
            height=player.height,
            weight=player.weight,
            age=player.age,
            college=player.college
        )

        # execution
        result = self.conn.execute(ins_query)
        # print(result)
        # print(type(result))

        # commit
        self.conn.commit()

        return result

    """
    function to modify a player, making use of the player model
    @param player: the PlayerModel representation of a player
    @param player_id: the player id
    @return result: the Cursor result 
    """
    def modify_player(self, player: PlayerModel, player_id: str):

        # create a dictionary with the updated player information
        # the player_id is fixed and can't be changed, even if user
        # can try to do that in the API docs

        # this will be depended by the input on fastAPI doc
        update_data = {
            "name": player.name,
            "position": player.position,
            "number": player.number,
            "current_Team": player.current_Team,
            "height": player.height,
            "weight": player.weight,
            "age": player.age,
            "college": player.college
        }

        # update query
        update_query = self.player_basic.update().where(self.player_basic.columns.player_id == player_id).values(update_data)

        # execute
        result = self.conn.execute(update_query)

        # commit
        self.conn.commit()

        return result

    """
    function to delete a player from the player_basic table by id
    @param id: the player id
    @return result: the Cursor result 
    """
    def delete_player(self, id: str):

        # delete query
        del_query = self.player_basic.delete().where(self.player_basic.columns.player_id == id)

        # execute
        result = self.conn.execute(del_query)

        # commit
        self.conn.commit()

        return result

