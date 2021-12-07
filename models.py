from database import db


class Tool(db.Model):
    __tablename__ = 'Tool'
    srnum = db.Column('SrNumber', db.Integer, primary_key=True, autoincrement=True)
    tool_height = db.Column('ToolHeight', db.Integer, nullable=False)
    tool_type = db.Column('ToolType', db.String)


class Standard(db.Model):
    __tablename__ = 'Standard'
    srnums = db.Column('SrNumber', db.Integer, autoincrement=True, primary_key=True)
    tool_type_code = db.Column('ToolTypeCode', db.Integer, db.ForeignKey("Tool.SrNumber"))
    length = db.Column('Length', db.Integer, nullable=False)
    code = db.Column('Code', db.String, unique=True)
    description = db.Column('Description', db.String)


class final_list(db.Model):
    __table__name = "final_list"
    srnumf = db.Column('SrNumber', db.Integer, autoincrement=True, primary_key=True)
    sk = db.Column('SK', db.Integer)

class User(db.Model):
    __table__name = "user"
    userid = db.Column("UserID", db.Integer, autoincrement=True, primary_key=True)
    useremail = db.Column("UserEmail", db.String)
    userpass = db.Column("Password", db.String)


class End_list(db.Model):
    __table__name = "end_list"
    srnuml = db.Column('SrNumber', db.Integer, autoincrement=True, primary_key=True)
    sk = db.Column('SK', db.Integer)
    quantity = db.Column('Quantity', db.Integer)
    length = db.Column('Length', db.Integer)
    toolcode = db.Column('ToolCode', db.Integer)
