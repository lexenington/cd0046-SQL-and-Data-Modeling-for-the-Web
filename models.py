from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
# from yaml import serialize



db = SQLAlchemy()


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    website = db.Column(db.String(250))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500), nullable=True)
    shows = db.relationship('Show', backref='venue', lazy=True )

    def __repr__(self):
        return f'<{self.id}, {self.name}>'

    @property
    def genres_list(self):
        genres = self.genres[1:-1]
        return''.join(genres).split(',')


    @property
    def upcoming_shows(self):
        # TODO: get up coiming shows functionality
        coming_shows = Show.query.filter(Show.start_time > datetime.now(), Show.venue_id == self.id).all()
        return coming_shows

    @property
    def past_shows(self):
        previous_shows = Show.query.filter(Show.start_time < datetime.now(), Show.venue_id == self.id).all()
        return previous_shows

    @property
    def filter_shows_by_city(self):
        # TODO: make venues list id, venue name and coming shows
        return {'city': self.city,
                'state': self.state,
                'venues': [(v.id, v.name, len(v.upcoming_shows))for v in Venue.query.filter(Venue.city == self.city, Venue.state == self.state).all()]}

    @property
    def serialize_venues(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'address': self.address,
            'phone': self.phone,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'genres': self.genres,
            'website': self.website,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
            'past_shows': self.past_shows,
            'upcoming_shows': self.upcoming_shows,
            'past_shows_count': len(self.past_shows),
            'upcoming_shows_count': len(self.upcoming_shows)

        }

    @property
    def serialize_for_edit(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'address': self.address,
            'phone': self.phone,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'genres': self.genres,
            'website': self.website,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
            'shows': self.shows

        }
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(250))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500), nullable=True)
    shows = db.relationship('Show', backref='artist', lazy=True )

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

    @property
    def genres_list(self):
        genres = self.genres[1:-1]
        return''.join(genres).split(',')

    @property
    def serialize_artists(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'genres': self.genres,
            'image_link': self.image_link,
            'website': self.website,
            'facebook_link': self.facebook_link,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            'past_shows': self.past_shows,
            'upcoming_shows': self.upcoming_shows,
            'past_shows_count': len(self.past_shows),
            'upcoming_shows_count': len(self.upcoming_shows)
        }

    @property
    def serialize_for_edit(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'genres': self.genres,
            'image_link': self.image_link,
            'website': self.website,
            'facebook_link': self.facebook_link,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            'shows': self.shows,
        }

    @property
    def upcoming_shows(self):
        # TODO: get up coiming shows functionality
        coming_shows = Show.query.filter(Show.start_time > datetime.now(), Show.artist_id == self.id).all()
        return coming_shows

    @property
    def past_shows(self):
        previous_shows = Show.query.filter(Show.start_time < datetime.now(), Show.artist_id == self.id).all()
        return previous_shows

    @property
    def artist_summary(self):
        # TODO: make venues list id, venue name and coming shows
        return {'id': self.id,
                'name': self.name,
                'num_upcoming_shows': len(self.upcoming_shows)}

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    start_time = db.Column(db.DateTime(), nullable=False)

    def __repr__(self):
        return f'{self.artist_id}, {self.start_time}'

    @property
    def serialize_shows(self):
        return {
            'venue_id': self.venue_id,
            'venue_name': self.venue.name,
            'artist_id': self.artist_id,
            'artist_name': self.artist.name,
            'artist_image_link': self.artist.image_link,
            'start_time': self.start_time
        }