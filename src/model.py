from src.extensions import db
import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    logs = db.relationship('LogItem', backref='user', lazy=True)

    @classmethod
    def insert(cls, name, password):
        '''
        class method that inserts a user into the database
        ----------
        args:
            name - string, name of the user
            passowrd - string, password used for sign in
            photo - string, location of the users's photo
        '''
        try:
            user = User(name=name, password=password)
            db.session.add(user)
            db.session.commit()
            print("successfully inserted a user into database")
        except:
            print("Error occured while inserting to database")

    @classmethod
    def update(cls, id, name, password, photo):
        '''
        class method that updates a specific user in the database
        ----------
        args:
            id - int
            name - string, name of the user
            passowrd - string, password used for sign in
            photo - string, location of the users's photo
        '''
        try:
            toEditRecord = cls.query.filter_by(id=id).first()
            toEditRecord.name = name
            toEditRecord.password = password
            toEditRecord.photo = photo
            db.session.commit()
            print(f"Successfully updated database")
        except:
            print("Error occured while updating database")

    @classmethod
    def delete(cls, id):
        '''
        class method that deletes a specific record in the database
        ----------
        args:
            id - int
        '''
        try:
            toDeleteRecord = cls.query.filter_by(id=id).first()
            db.session.delete(toDeleteRecord)
            db.session.commit()
            print(f"Successfully deleted item from database")
        except:
            print("Error occured while deleting from database")

    @classmethod
    def get(cls, id):
        '''
        class method that gets a specific record from database
        ----------
        args:
            id - int
        '''
        try:
            todo = cls.query.filter_by(id=id).first()
            print("Success retreiving data from database")
            return todo
        except:
            print("Error occured while retrieving from database")
            return None

    @classmethod
    def getAll(cls):
        '''
        class method that gets all records in database
        ----------
        '''
        try:
            todos = cls.query.all()
            print("Success retreiving data from database")
            return todos
        except:
            print("Error occured while retrieving from database")
            return None

    @classmethod
    def auth(cls, id, password):
        '''
        class method that auth a user with id and password
        ----------
        args:
            id - Integer
            passowrd - string
        '''
        try:
            user = User.get(id)
            if user:
                return True
        except:
            print("Error occured")

        return False


class LogItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    userID = db.Column(db.String, db.ForeignKey(User.id), nullable=True)
    dateCreated = db.Column(db.String(50), nullable=False,
                            default=str(datetime.datetime.utcnow().strftime("%c")))
    accepted = db.Column(db.Boolean, nullable=False)

    @classmethod
    def insert(cls, userID, accepted):
        '''
        class method that inserts a logItem into the database
        ----------
        args:
            userID - Integer, Foriegn key of the users database
            accepted - boolean, Shows if user was authenticated or not
            Photo - string, location to taken photo of the log
        '''
        try:
            logItem = LogItem(userID=userID, accepted=accepted)

            db.session.add(logItem)
            db.session.commit()
            print("successfully inserted a logitem into database")
            return logItem
        except:
            print("Error occured while inserting to database")

    @classmethod
    def get(cls, id):
        '''
        class method that gets a specific record from database
        ----------
        args:
            id - int
        '''
        try:
            logItem = cls.query.filter_by(id=id).first()
            print("Success retreiving data from database")
            return logItem
        except:
            print("Error occured while retrieving from database")
            return None

    @classmethod
    def getAll(cls):
        '''
        class method that gets all records in database
        ----------
        '''
        try:
            logItems = cls.query.all()
            print("Success retreiving data from database")
            return logItems
        except:
            print("Error occured while retrieving from database")
            return None
