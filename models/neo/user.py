from neomodel import ( StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, RelationshipTo, Relationship, RelationshipFrom)

# from user_meta import UserMeta

# from .user import User

class User(StructuredNode):
    email = StringProperty(unique_index=True, required=True)
    connections = Relationship('models.neo.user.User', 'CONNECTION')
    follows = RelationshipTo('models.neo.user.User', 'FOLLOW')
    connection_requests = RelationshipFrom('models.neo.user.User', 'REQUEST')

