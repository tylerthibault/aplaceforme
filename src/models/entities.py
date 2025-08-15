from __future__ import annotations

import base64
import os
import secrets
from datetime import datetime
from typing import Optional

from flask_login import UserMixin
from server import bcrypt

from server import db


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SlugMixin:
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)


def b64_encode_filebytes(data: bytes) -> str:
    if not data:
        return ""
    return base64.b64encode(data).decode("utf-8")


def b64_decode_to_bytes(data_b64: str) -> bytes:
    if not data_b64:
        return b""
    return base64.b64decode(data_b64)


story_tags = db.Table(
    "story_tags",
    db.Column("story_id", db.Integer, db.ForeignKey("stories.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)

testimonial_tags = db.Table(
    "testimonial_tags",
    db.Column("testimonial_id", db.Integer, db.ForeignKey("testimonials.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)

music_tags = db.Table(
    "music_tags",
    db.Column("music_id", db.Integer, db.ForeignKey("music_tracks.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)


class Tag(TimestampMixin, db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    slug = db.Column(db.String(160), nullable=False, unique=True, index=True)


class Story(TimestampMixin, SlugMixin, db.Model):
    __tablename__ = "stories"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.Text)
    body = db.Column(db.Text)  # rich-ish HTML allowed (sanitized on render)
    author_name = db.Column(db.String(120))
    cover_image_b64 = db.Column(db.Text)  # base64 string
    is_published = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime)
    tags = db.relationship("Tag", secondary=story_tags, backref="stories")


class Testimonial(TimestampMixin, SlugMixin, db.Model):
    __tablename__ = "testimonials"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    quote = db.Column(db.String(500))
    body = db.Column(db.Text)
    person_name = db.Column(db.String(120))
    location = db.Column(db.String(120))
    cover_image_b64 = db.Column(db.Text)
    is_published = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime)
    tags = db.relationship("Tag", secondary=testimonial_tags, backref="testimonials")


class MusicTrack(TimestampMixin, SlugMixin, db.Model):
    __tablename__ = "music_tracks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    artist_name = db.Column(db.String(120))
    description = db.Column(db.Text)
    audio_b64 = db.Column(db.Text)  # base64 audio content
    cover_image_b64 = db.Column(db.Text)
    duration_sec = db.Column(db.Integer)
    is_published = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime)
    tags = db.relationship("Tag", secondary=music_tags, backref="music_tracks")


class Subscriber(TimestampMixin, db.Model):
    __tablename__ = "subscribers"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120))
    status = db.Column(db.String(20), default="active")  # pending|active|unsubscribed
    unsubscribe_token = db.Column(db.String(64), unique=True, index=True, default=lambda: secrets.token_urlsafe(32))
    confirmed_at = db.Column(db.DateTime)
    unsubscribed_at = db.Column(db.DateTime)


class NewsletterIssue(TimestampMixin, db.Model):
    __tablename__ = "newsletter_issues"
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    body_html = db.Column(db.Text)
    body_text = db.Column(db.Text)
    sent_at = db.Column(db.DateTime)


class AdminUser(UserMixin, TimestampMixin, db.Model):
    __tablename__ = "admin_users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password: str):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)


def get_or_create_admin(username: str, password: Optional[str] = None) -> AdminUser:
    user = AdminUser.query.filter_by(username=username).first()
    if user:
        return user
    user = AdminUser(username=username)
    user.set_password(password or os.environ.get("ADMIN_PASSWORD", "change-me"))
    db.session.add(user)
    db.session.commit()
    return user
