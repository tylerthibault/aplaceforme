from __future__ import annotations

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from sqlalchemy import desc
from datetime import datetime

from server import db
from src.controllers.forms import SubscribeForm, LoginForm
from src.models.entities import Story, Testimonial, MusicTrack, Subscriber, AdminUser
from src.utils.sanitization import sanitize_html

public_bp = Blueprint("public", __name__)
admin_bp = Blueprint("admin", __name__)


@public_bp.route("/")
def landing():
    stories = (
        Story.query.filter_by(is_published=True)
        .order_by(desc(Story.published_at), desc(Story.created_at))
        .limit(3)
        .all()
    )
    testimonials = (
        Testimonial.query.filter_by(is_published=True)
        .order_by(desc(Testimonial.published_at), desc(Testimonial.created_at))
        .limit(3)
        .all()
    )
    latest_track = (
        MusicTrack.query.filter_by(is_published=True)
    .order_by(desc(MusicTrack.published_at), desc(MusicTrack.created_at))
        .first()
    )
    form = SubscribeForm()
    return render_template("public/landing/index.html", stories=stories, testimonials=testimonials, latest_track=latest_track, form=form)


@public_bp.route("/stories")
def list_stories():
    page = max(int(request.args.get("page", 1)), 1)
    per_page = 10
    pagination = (
        Story.query.filter_by(is_published=True)
        .order_by(desc(Story.published_at), desc(Story.created_at))
        .paginate(page=page, per_page=per_page, error_out=False)
    )
    return render_template("public/stories/list.html", pagination=pagination)


@public_bp.route("/stories/<slug>")
def story_detail(slug: str):
    story = Story.query.filter_by(slug=slug, is_published=True).first_or_404()
    story.body = sanitize_html(story.body or "")
    return render_template("public/stories/detail.html", story=story)


@public_bp.route("/testimonials")
def list_testimonials():
    page = max(int(request.args.get("page", 1)), 1)
    per_page = 10
    pagination = (
        Testimonial.query.filter_by(is_published=True)
        .order_by(desc(Testimonial.published_at), desc(Testimonial.created_at))
        .paginate(page=page, per_page=per_page, error_out=False)
    )
    return render_template("public/testimonials/list.html", pagination=pagination)


@public_bp.route("/testimonials/<slug>")
def testimonial_detail(slug: str):
    t = Testimonial.query.filter_by(slug=slug, is_published=True).first_or_404()
    t.body = sanitize_html(t.body or "")
    return render_template("public/testimonials/detail.html", testimonial=t)


@public_bp.route("/music")
def music_list():
    tracks = (
        MusicTrack.query.filter_by(is_published=True)
        .order_by(desc(MusicTrack.published_at), desc(MusicTrack.created_at))
        .all()
    )
    return render_template("public/music/list.html", tracks=tracks)


@public_bp.route("/subscribe", methods=["GET", "POST"])
def subscribe():
    form = SubscribeForm()
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        name = (form.name.data or "").strip()
        existing = Subscriber.query.filter_by(email=email).first()
        if existing and existing.status == "active":
            flash("You're already subscribed.", "info")
            return redirect(url_for("public.landing"))
        if not existing:
            s = Subscriber(email=email, name=name, status="active", confirmed_at=datetime.utcnow())
            db.session.add(s)
        else:
            existing.status = "active"
            existing.unsubscribed_at = None
        db.session.commit()
        flash("Subscribed!", "success")
        return redirect(url_for("public.landing"))
    return render_template("public/subscribe.html", form=form)


@public_bp.route("/unsubscribe/<token>")
def unsubscribe(token: str):
    s = Subscriber.query.filter_by(unsubscribe_token=token).first_or_404()
    s.status = "unsubscribed"
    s.unsubscribed_at = datetime.utcnow()
    db.session.commit()
    return render_template("public/unsubscribed.html")


@public_bp.route("/search")
def search():
    q = (request.args.get("q") or "").strip()
    results = {"stories": [], "testimonials": [], "music": []}
    if q:
        like = f"%{q}%"
        results["stories"] = Story.query.filter(Story.is_published == True, (Story.title.ilike(like) | Story.summary.ilike(like))).limit(10).all()
        results["testimonials"] = Testimonial.query.filter(Testimonial.is_published == True, (Testimonial.title.ilike(like) | Testimonial.quote.ilike(like))).limit(10).all()
        results["music"] = MusicTrack.query.filter(MusicTrack.is_published == True, MusicTrack.title.ilike(like)).limit(10).all()
    return render_template("public/search.html", q=q, results=results)


# Admin
@admin_bp.route("/")
@login_required
def admin_index():
    subs_count = Subscriber.query.count()
    stories_count = Story.query.count()
    testimonials_count = Testimonial.query.count()
    music_count = MusicTrack.query.count()
    return render_template("private/index.html", stats={
        "subscribers": subs_count,
        "stories": stories_count,
        "testimonials": testimonials_count,
        "music": music_count,
    })


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = AdminUser.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("admin.admin_index"))
        flash("Invalid credentials", "danger")
    return render_template("private/login.html", form=form)


@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("public.landing"))
