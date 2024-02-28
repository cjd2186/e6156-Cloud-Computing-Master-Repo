from pydantic import BaseModel
import sqlalchemy as db_al
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define Pydantic data model for a coach
class CoachModel(BaseModel):
    id: int
    name: str
    team: str = None
    birthdate: str = None
    startdate: int = None
    enddate: str = None
    email: str = None
    wins: int = None
    losses: int = None

# Class to interact with the database for coach-related operations
class CoachResource:
    def __init__(self):
        db_username = os.getenv("DB_USERNAME")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = str(os.getenv("DB_PORT"))
        db_name = os.getenv("DB_NAME")

        # Create a SQLAlchemy engine
        #db_url = fcd micr"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
        db_url = f"mysql+mysqlconnector://doe2102:sql_for_mgmt@34.23.76.102/Managers"
        self.engine = db_al.create_engine(db_url)
        self.conn = self.engine.connect()

        # Metadata instance for extracting the metadata: structures, table infos, etc.
        self.metadata = db_al.MetaData()

        # Table object for the coaches table
        self.coaches_table = db_al.Table('Head_Coaches', self.metadata, autoload_with=self.engine)

    def get_coach_by_id(self, coach_id):
        query = self.coaches_table.select().where(self.coaches_table.columns.id == coach_id)
        exe = self.conn.execute(query)
        #result = exe.fetchone()
        #return result

        column_names = exe.keys()
        result = exe.fetchall()
        result_dicts = [dict(zip(column_names, row)) for row in result]

        return result_dicts

    def get_paginated_coaches(self, limit, offset):
        query = self.coaches_table.select().limit(limit).offset(offset)
        exe = self.conn.execute(query)

        column_names = exe.keys()
        result = exe.fetchall()
        result_dicts = [dict(zip(column_names, row)) for row in result]

        return result_dicts

    def add_coach(self, coach: CoachModel):
        ins_query = self.coaches_table.insert().values(
            id=coach.id,
            name=coach.name,
            team=coach.team,
            birthdate=coach.birthdate,
            startdate=coach.startdate,
            enddate=coach.enddate,
            email=coach.email,
            wins=coach.wins,
            losses=coach.losses
        )
        result = self.conn.execute(ins_query)
        self.conn.commit()
        return result

    def modify_coach(self, coach: CoachModel, coach_id: int):
        update_data = {
            "name": coach.name,
            "team": coach.team,
            "birthdate": coach.birthdate,
            "startdate": coach.startdate,
            "enddate": coach.enddate,
            "email": coach.email,
            "wins": coach.wins,
            "losses": coach.losses
        }
        update_query = self.coaches_table.update().where(self.coaches_table.columns.id == coach_id).values(update_data)
        result = self.conn.execute(update_query)
        self.conn.commit()
        return result

    def delete_coach(self, coach_id):
        del_query = self.coaches_table.delete().where(self.coaches_table.columns.id == coach_id)
        result = self.conn.execute(del_query)
        self.conn.commit()
        return result
