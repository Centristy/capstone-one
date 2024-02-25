from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Profile Image URL')

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class UserEditForm(FlaskForm):
    """Form for editing users."""
    username = StringField('Username')
    email = StringField('E-mail', validators=[Email()])
    image_url = StringField('(Optional) Image URL')
    header_image_url = StringField('(Optional) Profile Image URL')
    password = PasswordField('Password', validators=[Length(min=6)])

class DeckAddForm(FlaskForm):
    """Form for adding a Deck."""
    title = StringField('Title', validators=[DataRequired()])
    cover_img = StringField('(Optional) Cover Image URL')

class CardAddForm(FlaskForm):
    """Form for adding a Card to a Deck."""
    english = StringField('English', validators=[DataRequired()])
    korean = StringField('Korean', validators=[DataRequired()])
    image_url = StringField('(Optional) Card Image URL')