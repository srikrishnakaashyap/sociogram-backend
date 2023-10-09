from models.mongo.user import User
from models.neo.user import User as GraphUser
from neomodel import match,Traversal
from models.mongo.user import User
class Neo4jService:
   
    # Normal user to GraphUser
    #GraphUser to a normalUser
    @classmethod
    def user_to_graph_user(cls, user=None, email=None):
        email = email or user.email
        graph_user = GraphUser.nodes.get(email=email)
        return graph_user


    @classmethod
    async def graph_user_to_user(cls, graph_user):
        user_object = await User.find_one(User.email == graph_user.email)
        return user_object

    @classmethod
    def serialize_user(cls, user_object):
        return {"email": user_object.email, "name": user_object.name}
    
    @classmethod
    async def graph_users_to_users(cls, graph_user_list):
        user_list = []
        for graph_user in graph_user_list:
            user_list.append(await cls.graph_user_to_user(graph_user))
        return user_list
    
    @classmethod
    async def all_connections(cls, user):
        graph_user = cls.user_to_graph_user(user=user)
        definition = dict(node_class=GraphUser, direction= match.EITHER,
                  relation_type='CONNECTION')
        connections_traversal = Traversal(graph_user, GraphUser.__label__,
                                definition)
        all_user_connections = connections_traversal.all()
        return all_user_connections
        
    
    @classmethod
    async def serialize(cls,users):
        response_objects = []
        for connection in users:
            user_object = await cls.graph_user_to_user(connection)
            response_objects.append({"email": user_object.email, "name": user_object.name})
        return response_objects

            
