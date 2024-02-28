# partially based on https://www.youtube.com/watch?v=ZUrNFhG3LK4&ab_channel=MaheshKariya
import graphene
from resources.teamdata import teams

# define the graphene objectType for team right here instead of a separate serializer file
class TeamType(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    city = graphene.String()
    mascot = graphene.String()
    found_year = graphene.Int()
    mascot_type = graphene.String()

# define query
class TeamQuery(graphene.ObjectType):
    team_by_id = graphene.List(TeamType, id=graphene.String())
    team_by_name = graphene.List(TeamType, name=graphene.String())
    team_by_mascot_type = graphene.List(TeamType, mascot_type=graphene.String())
    #resolvers
    @staticmethod
    def resolve_team_by_id(self, info, id):
        return list(filter(lambda team: team["id"]==id, teams))

    def resolve_team_by_name(self, info, name):
        return list(filter(lambda team: team["name"] == name, teams))

    @staticmethod
    def resolve_team_by_mascot_type(self, info, mascot_type):
        return list(filter(lambda team: team["mascot_type"]==mascot_type, teams))