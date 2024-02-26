import os

from flask import Flask, render_template, request, flash, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
from translate import Translator

from forms import UserAddForm, LoginForm, UserEditForm, DeckAddForm, CardAddForm
from models import db, connect_db, User, Deck, Card, bcrypt

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
os.environ.get('DATABASE_URL', 'postgresql:///hanguldex'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

toolbar = DebugToolbarExtension(app)

translator = Translator(provider='libre', from_lang='en', to_lang='kr')


connect_db(app)



@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None



def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id



def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


# Landing Page has all the flash card decks and includes a modal to create a new deck


@app.route('/', methods=["GET", "POST"])
def homepage():
    """Show homepage:"""

    decks = (Deck.query.filter(Deck.user_id == g.user.id).all())

    form = DeckAddForm()

    if g.user:

        """Create a New Deck"""

        id = g.user.id

        if form.validate_on_submit():
            deck = Deck(
                title=form.title.data,
                cover_img=form.cover_img.data or Deck.cover_img.default.arg,
                user_id  = id
            )

            g.user.decks.append(deck)
            db.session.commit()

            flash("Deck Created!", 'success')

            return redirect(f"/decks/edit/{deck.id}")

        return render_template('home.html', decks=decks, form=form)

    else:
        
        return render_template('home-anon.html', form=form)
    

#Login form with bycrpt authentication


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


#Signup form with unique usernames


@app.route('/signup', methods=["GET", "POST"])
def  signup():

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
                header_image_url = User.header_image_url.default.arg
            )
            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)
    

#Allows users to edit profile information, profile pic and header image
    

@app.route('/edit', methods=["GET", "POST"])
def edit_profile():
    """Update profile for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.image_url = form.image_url.data or User.image_url.default.arg,
            user.header_image_url = form.header_image_url.data or User.header_image_url.default.arg,

            db.session.commit()
            return redirect(f"/")

        flash("Wrong password, please try again.", 'danger')

    return render_template('users/edit.html', form=form, user_id=user.id)


#Deletes users along with all cards and decks associated with user

@app.route('/delete', methods=["GET", "POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    

    Card.query.filter(Card.user_id == g.user.id).delete()
    Deck.query.filter(Deck.user_id == g.user.id).delete()



    db.session.delete(g.user)
    db.session.commit()

    flash("Account Successfully Deleted", "success")

    return redirect("/signup")


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/login")
    

##############################################################################
# Deck routes:

#Allows users to edit a deck

@app.route('/decks/edit/<int:deck_id>', methods=["GET", "POST"])
def edit_deck(deck_id):
    

    form = CardAddForm()
    deck = Deck.query.get_or_404(deck_id)
    cards = (Card
            .query
            .filter(Card.deck_id == deck.id)
            .all())
    
    if form.validate_on_submit():
        
        card = Card.add(
                english=form.english.data,
                korean=form.korean.data,
                image_url=form.image_url.data or Card.image_url.default.arg,
                deck_id = deck_id,
                user_id = g.user.id
            )
        
        db.session.add(card)

        db.session.commit()

        flash("Card Added", 'success')

        return redirect(f'/decks/edit/{deck_id}')
    
    else:

        return render_template('decks/editdeck.html', deck=deck, form=form, cards=cards)
    

#Allows user to delete a deck

@app.route('/decks/delete/<int:deck_id>', methods=["GET", "POST"])
def delete_deck(deck_id):
    


    Card.query.filter(Card.deck_id == deck_id).delete()
    Deck.query.filter(Deck.id == deck_id).delete()

    db.session.commit()
        
    return redirect(f'/')

#Allows user to delete a specific card

@app.route('/decks/delete/card/<int:card_id>', methods=["GET", "POST"])
def delete_card(card_id):



    card = Card.query.get_or_404(card_id)
    deck_id = card.deck_id
    db.session.delete(card)
    db.session.commit()
        
    return redirect(f'/decks/edit/{deck_id}')
    



@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req