from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

basedir = 'reporting_systems'

app = Flask(__name__)
app.secret_key = 'IM_THE_BEST'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + '../database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

devices_in_room = db.Table(
    'devices_in_room',
    db.Column('device_id', db.Integer, db.ForeignKey('device.id'), primary_key=True),
    db.Column('room_id', db.Integer, db.ForeignKey('room.id'), primary_key=True)
)


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(50), unique=True, nullable=False)
    IP = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, device_name, IP, status):
        self.device_name = device_name
        self.IP = IP
        self.status = status

    def save(self):
        db.session.add(self)
        db.session.commit()


class DeviceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Device
        include_relationships = True
        load_instance = True


device_schema = DeviceSchema()
devices_schema = DeviceSchema(many=True)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(50), unique=True, nullable=False)
    devices = db.relationship('Device', secondary=devices_in_room, backref='rooms')

    def __init__(self, room_name):
        self.room_name = room_name

    def save(self):
        db.session.add(self)
        db.session.commit()


class RoomSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Room
        include_relationships = True
        load_instance = True


room_schema = RoomSchema()
rooms_schema = RoomSchema(many=True)





class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String)
    face = db.Column(db.LargeBinary)

    def __init__(self, username, password, face):
        self.username = username
        self.password = password
        self.face = face

    def save(self):
        db.session.add(self)
        db.session.commit()


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True


user_schema = UserSchema()
users_schema = UserSchema(many=True)
