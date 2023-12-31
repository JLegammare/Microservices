from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(required=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)