import datetime as dt

from sqlalchemy import (
    Column,
    Unicode,
    UnicodeText,
    CHAR,
    String,
    Text,
    Integer,
    ForeignKey,
    Date,
    DateTime,
    Enum,
    Boolean,
    UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship, synonym

""" Eve exspects the resource names to be equal to the table names. Therefore
we generate all names from the Class names. Please choose classnames carefully,
as changing them might break a lot of code """


class BaseModel(object):
    """Mixin for common columns."""

    """__abstract__ makes SQL Alchemy not create a table for this class """
    __abstract__ = True

    """ All classes which overwrite this with True will get exposed as a
    resource """
    __expose__ = False

    """For documentation"""
    __description__ = {}

    """ This is a list of fields, which are added to the projection created by
    eve. Add any additional field to be delivered on GET requests by default
    in the subclasses. """
    __projected_fields__ = []

    __public_methods__ = []
    __owner_methods__ = []
    __registered_methods__ = []

    @declared_attr
    def __tablename__(cls):
        """ Correct English attaches 'es' to plural forms which end in 's' """
        if cls.__name__.lower()[-1:] == 's':
            return "%ses" % cls.__name__.lower()
        return "%ss" % cls.__name__.lower()

    id = Column(Integer, primary_key=True, autoincrement=True)

    @declared_attr
    def _id(cls):
        return synonym("id")

    _created = Column(DateTime, default=dt.datetime.utcnow)
    _updated = Column(
        DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow)
    _etag = Column(String(50))

    """ This needs to be a function, as it has a ForeignKey in a mixin. The
    function makes binding at a later point possible """
    @declared_attr
    def _author(cls):
        return Column(Integer, ForeignKey("users.id"))  # , nullable=False)


Base = declarative_base(cls=BaseModel)


class User(Base):
    __description__ = {
        'general': "In general, the user data will be generated from "
        "LDAP-Data. However, one might change the RFID-Number or the "
        "membership-status. Extraordinary members may not have a LDAP-Account "
        "and can therefore access all given fields.",
        'methods': {
            'GET': "Authorization is required for most of the fields"
        }}
    __expose__ = True
    __projected_fields__ = ['permissions']

    __owner__ = ['id']
    __owner_methods__ = ['GET', 'PATCH']

    username = Column(CHAR(50), unique=True, nullable=False)
    password = Column(CHAR(100))  # base64 encoded hash data
    firstname = Column(Unicode(50), nullable=False)
    lastname = Column(Unicode(50), nullable=False)
    birthday = Column(Date)
    legi = Column(CHAR(8))
    rfid = Column(CHAR(6))
    nethz = Column(String(30))
    department = Column(Enum("itet", "mavt"))
    phone = Column(String(20))
    ldapAddress = Column(Unicode(200))
    gender = Column(Enum("male", "female"), nullable=False)
    email = Column(CHAR(100), nullable=False, unique=True)
    membership = Column(Enum("none", "regular", "extraordinary", "honorary"),
                        nullable=False, default="none", server_default="none")

    """relationships"""
    permissions = relationship("Permission", foreign_keys="Permission.user_id",
                               backref="user", cascade="all, delete")
    forwards = relationship("ForwardUser", foreign_keys="ForwardUser.user_id",
                            backref="user", cascade="all, delete")
    sessions = relationship("Session", foreign_keys="Session.user_id",
                            backref="user", cascade="all, delete")
    eventsignups = relationship("_EventSignup",
                                foreign_keys="_EventSignup.user_id",
                                backref="user", cascade="all, delete")


class Permission(Base):
    """Intermediate table for 'many-to-many' mapping
        split into one-to-many from Group and many-to-one with User
    We need to use a class here in stead of a table because of additional data
        expiry_date
    """
    __expose__ = True

    __owner__ = ['user_id']
    __owner_methods__ = ['GET']

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(CHAR(20), nullable=False)
    expiry_date = Column(DateTime)

    # user = relationship("User", foreign_keys=user_id, backref="permissions")


class Forward(Base):
    __description__ = {
        'general': "This resource describes the different email-lists. To see "
        "the subscriptions, have a look at '/forwardusers' and "
        "'forwardaddresses'.",
        'fields': {
            'is_public': "A public Forward can get subscriptions from external"
            " users. If False, only AMIV-Members can subscribe to this list."
        }}
    __expose__ = True
    __projected_fields__ = ['user_subscribers', 'address_subscribers']

    __owner__ = ['owner_id']
    __owner_methods__ = ['GET', 'DELETE']

    address = Column(Unicode(100), unique=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_public = Column(Boolean, default=False, nullable=False)

    owner = relationship(User, foreign_keys=owner_id)

    """relationships"""
    user_subscribers = relationship("ForwardUser", backref="forward",
                                    cascade="all, delete")
    address_subscribers = relationship("_ForwardAddress", backref="forward",
                                       cascade="all, delete")


class ForwardUser(Base):
    __expose__ = True
    __projected_fields__ = ['forward', 'user']

    __owner__ = ['user_id', 'forward.owner_id']
    __owner_methods__ = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                     nullable=False)
    forward_id = Column(
        Integer, ForeignKey("forwards.id", ondelete="CASCADE"), nullable=False)

    # forward = relationship("Forward", backref="user_subscribers")
    # user = relationship("User", foreign_keys=user_id)


class _ForwardAddress(Base):
    __expose__ = True
    __projected_fields__ = ['forward']

    __owner__ = ['forward.owner_id']
    __owner_methods__ = ['GET', 'POST', 'DELETE']
    __public_methods__ = ['POST', 'DELETE']

    address = Column(Unicode(100))
    forward_id = Column(
        Integer, ForeignKey("forwards.id"), nullable=False)

    # forward = relationship("Forward", backref="address_subscribers")


class Session(Base):
    __expose__ = True
    __projected_fields__ = ['user']

    __public_methods__ = ['POST']
    __owner__ = ['user_id']
    __owner_methods__ = ['GET', 'DELETE']

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(CHAR(512), unique=True)

    # user = relationship("User", foreign_keys=user_id, backref="sessions")


class Event(Base):
    __description__ = {
        'fields': {
            'price': 'Price of the event as Integer in Rappen.',
            'additional_fields': "must be provided in form of a JSON-Schema.",
            'is_public': "If False, only AMIV-Members can sign up for this "
            "event",
            'spots': "For no limit, set to '0'. If no signup required, set to "
            "'-1'.",
        }
    }
    __expose__ = True
    __projected_fields__ = ['signups']

    __public_methods__ = ['GET']

    time_start = Column(DateTime)
    time_end = Column(DateTime)
    location = Column(Unicode(50))
    is_public = Column(Boolean, default=False, nullable=False)
    price = Column(Integer)  # Price in Rappen
    spots = Column(Integer, nullable=False)
    time_register_start = Column(DateTime)
    time_register_end = Column(DateTime)
    additional_fields = Column(Text)
    # Images
    img_thumbnail = Column(CHAR(100))  # This will be modified in schemas.py!
    img_web = Column(CHAR(100))  # This will be modified in schemas.py!
    img_1920_1080 = Column(CHAR(100))  # This will be modified in schemas.py!

    """Translatable fields
    The relationship exists to ensure cascading delete and will be hidden from
    the user
    """
    title_id = Column(Integer, ForeignKey('translationmappings.id'))
    title_rel = relationship("TranslationMapping", cascade="all, delete",
                             foreign_keys=title_id)
    description_id = Column(Integer, ForeignKey('translationmappings.id'))
    description_rel = relationship("TranslationMapping", cascade="all, delete",
                                   foreign_keys=description_id)

    """relationships"""
    signups = relationship("_EventSignup", backref="event",
                           cascade="all, delete")


class _EventSignup(Base):
    __description__ = {
        'fields': {
            'extra_data': "Data-schema depends on 'additional_fields' from the"
            " mapped event.",
            'user_id': "To sign up as external user, set 'user_id' to '-1'",
            'email': "If empty, the api fills this with the standard-email of "
            "the user. This field is required for external users.",
        }}
    __expose__ = True
    __projected_fields__ = ['event', 'user']

    __owner__ = ['user_id']
    __owner_methods__ = ['POST', 'GET', 'PATCH', 'DELETE']
    # __public_methods__ = ['POST']

    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    email = Column(Unicode(100))
    extra_data = Column(Text)

    """Data-Mapping: many-to-one"""
    # user = relationship("User", foreign_keys=user_id)

    """Data-Mapping: many-to-one"""
    # event = relationship("Event", backref="signups")


class File(Base):
    """This is a file that belongs to a study document.

    An additional name for the file is possible
    A studydocument needs to be referenced

    Files can only be created and deleted (or both, put), patching them is not
    intended
    """
    __expose__ = True

    __owner__ = ['_author']  # This permitts everybody to post here!
    __owner_methods__ = ['GET', 'POST', 'PUT', 'DELETE']
    __registered_methods__ = ['GET']

    name = Column(Unicode(100))
    data = Column(CHAR(100))  # This will be modified in schemas.py!
    study_doc_id = Column(Integer, ForeignKey("studydocuments.id"),
                          nullable=False)
    # study_doc = relationship("StudyDocument", backref="files")


class StudyDocument(Base):
    __expose__ = True
    __projected_fields__ = ['files']

    __owner__ = ['_author']
    __owner_methods__ = ['GET', 'PUT', 'POST', 'PATCH', 'DELETE']
    __registered_methods__ = ['GET']

    name = Column(Unicode(100))
    type = Column(String(30))
    exam_session = Column(String(10))
    department = Column(Enum("itet", "mavt"))
    lecture = Column(Unicode(100))
    professor = Column(Unicode(100))
    semester = Column(Integer)
    author_name = Column(Unicode(100))

    """relationships"""
    files = relationship("File", backref="study_doc",
                         cascade="all, delete")


class JobOffer(Base):
    __expose__ = True

    __public_methods__ = ['GET']

    company = Column(Unicode(30))

    logo = Column(CHAR(100))  # This will be modified in schemas.py!
    pdf = Column(CHAR(100))  # This will be modified in schemas.py!
    time_end = Column(DateTime)

    """Translatable fields
    The relationship exists to ensure cascading delete and will be hidden from
    the user
    """
    title_id = Column(Integer, ForeignKey('translationmappings.id'))
    title_rel = relationship("TranslationMapping", cascade="all, delete",
                             foreign_keys=title_id)
    description_id = Column(Integer, ForeignKey('translationmappings.id'))
    description_rel = relationship("TranslationMapping", cascade="all, delete",
                                   foreign_keys=description_id)


# Confirm Actions for unregistered email-adresses
class Confirm(Base):
    token = Column(CHAR(20), unique=True, nullable=False)
    method = Column(String(10))
    resource = Column(String(50))
    data = Column(String(1000))
    expiry_date = Column(DateTime)


# Permissions for file storage
class Storage:
    __expose__ = False  # Don't create a schema
    __registered_methods__ = ['GET']


class Roles:
    __expose__ = False  # Don't create a schema
    __registered_methods__ = ['GET']


# Language ids are in here
class TranslationMapping(Base):
    __expose__ = True

    content = relationship("Translation",
                           cascade="all, delete", uselist=True)


# This is the translated content
class Translation(Base):
    __expose__ = True

    localization_id = Column(Integer, ForeignKey('translationmappings.id'),
                             nullable=False)
    language = Column(Unicode(10), nullable=False)
    content = Column(UnicodeText, nullable=False)

    __table_args__ = (UniqueConstraint('localization_id', 'language'),)
