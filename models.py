from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )
    

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
    )

    header_image_url = db.Column(
        db.Text,
        default="/static/images/default-header.jpg"
    )


    decks = db.relationship('Deck')
    cards = db.relationship('Card')


    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Deck(db.Model):

    __tablename__ = 'decks'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    title = db.Column(
        nullable=False,
    )

    cover_img = db.Column(
        db.Text,
        default="/static/images/deck-cover.JPG",
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    cards = db.relationship('Card')




class Card(db.Model):

    __tablename__ = 'cards'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    english = db.Column(
        db.Text,
        nullable=False,
    )

    korean = db.Column(
        db.Text,
        nullable=True
    )

    image_url = db.Column(
        db.Text,
        default="/static/images/default-card.png",
    )

    deck_id = db.Column(
        db.Integer,
        db.ForeignKey('decks.id', ondelete='CASCADE'),
        nullable=False,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    @classmethod
    def add(cls, english, korean, image_url, deck_id, user_id):
        """Add a New Card """

        card = Card(

            english=english,
            korean=korean,
            image_url=image_url,
            deck_id=deck_id,
            user_id = user_id

        )
        return card




def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)