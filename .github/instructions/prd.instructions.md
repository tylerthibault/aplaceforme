---
applyTo: '**'
---
# Product Requirements Document (PRD) — Marla Baily Website

## 1) Summary

Create a simple, elegant website for Marla Baily to publish:
- God Stories (long-form testimonies/stories)
- God Testimonials (conversion testimonies; shorter narrative format)
- Music (her own or friends’ tracks)
- Newsletter sign-ups and newsletter delivery to subscribers

Tone and aesthetics: nature-forward, foresty/friendly with Apple-like polish. Use frosted glass (glassmorphism), rounded corners, generous whitespace, and subtle, tasteful animations. The site must be responsive and accessible.

Technical baseline: Python (Flask) + Jinja templates, SQLite (temporary) with SQLAlchemy ORM. CSS and JS are separate from HTML, with Jinja only where needed. Jinja templates/macros are used to componentize sections; avoid overusing macros. All media (images/audio) will be base64-encoded and stored in the SQLite DB for MVP.

Primary audience: visitors seeking to read God Stories/testimonials, listen to music, and subscribe to updates.

## 2) Goals and Non-Goals

Goals
- Publish and organize God Stories, Testimonials, and Music.
- Provide a clean, friendly, nature-inspired landing experience with subtle animations.
- Allow visitors to subscribe and receive newsletters.
- Keep codebase modular via Jinja includes and selective macros; CSS/JS separate from HTML.
- Use SQLite + SQLAlchemy for data, with migration path for future DB.

Non-Goals (for MVP)
- Full-featured CMS UI (we’ll implement a minimal authoring/admin area; advanced workflows can be future work).
- User accounts beyond subscribers (no public user profiles, comments, or logins for visitors).
- Complex e-commerce, donations, or merch (future consideration).

## 3) Personas

- Reader/Seeker: Wants to quickly find encouraging stories/testimonies; prefers clean typography and easy navigation.
- Listener: Wants to preview/play music, optionally read context.
- Subscriber: Wants to sign up easily and receive occasional newsletters.
- Marla (Author/Admin): Needs a straightforward way to post stories/testimonies/music and send newsletters.

## 4) Information Architecture & Navigation

Top-level navigation (desktop header, collapsible on mobile):
- Home
- God Stories
- Testimonials
- Music
- About
- Subscribe
- Contact

Footer: repeat key links, social links, copyright, privacy.

## 5) Content Types (Data Model Overview)

God Story
- id, title, slug, summary, body (rich text/Markdown-safe), author_name, cover_image, tags[], created_at, published_at, is_published

Testimonial
- id, title, slug, quote (short), body (narrative), person_name, location (optional), cover_image, tags[], created_at, published_at, is_published

Music Track
- id, title, slug, artist_name, description, audio_url or file, cover_image, tags[], created_at, published_at, is_published, duration_sec (optional)

Subscriber
- id, email (unique), name (optional), status (pending|active|unsubscribed), created_at, confirmed_at, unsubscribed_at, unsubscribe_token

Newsletter Issue
- id, subject, body_html (rendered), body_text (fallback), sent_at (nullable), created_at, updated_at

Tag
- id, name, slug, created_at

MediaAsset (optional, future)
- id, path/url, kind (image|audio|file), alt_text, created_at

## 6) Functional Requirements

Landing Page
- Hero section (forest-inspired background with frosted-glass overlay card).
- Featured sections: latest 3 God Stories, latest 3 Testimonials, and a Music teaser/player for most recent track.
- Subscribe call-to-action (CTA) block.
- Each section is a separate Jinja include to keep the landing template tidy.

God Stories
- Listing page with cards (image, title, summary, tags, date) and pagination.
- Detail page with cover image, author_name, date, tags, and body text.
- Social share meta and share links.

Testimonials
- Listing page with filter by tag and pagination.
- Detail page styled for quotes/narratives.

Music
- Listing grid with cover art and a simple, accessible HTML5 audio player.
- Detail page (optional in MVP) with description and related items.

Subscribe & Newsletter
- Subscribe page with email form (CSRF-protected). Optional name field.
- Double opt-in optional. MVP will use single opt-in (no confirmation email).
- Admin can draft and send newsletter issues to active subscribers.
- Unsubscribe link in all emails.

Search/Filter (MVP-light)
- Simple site-wide search box that queries titles/summaries across stories/testimonials/music (server-side LIKE-based search; future: full-text).

Admin/Authoring (MVP)
- Password-protected minimal admin (single admin user via env var credentials or simple auth) to:
  - Create/edit/publish God Stories
  - Create/edit/publish Testimonials
  - Create/edit/publish Music Tracks
  - Create/send Newsletter Issues
  - View subscriber count and statuses

## 7) Design & UX

Visual Style
- Forest/nature theme with greens and neutrals; glassmorphism panels: frosted glass (backdrop-filter blur), subtle translucency, soft shadows, rounded corners.
- Typography: Humanist sans for headings (e.g., system fallback with Apple-like tone), readable serif or sans for body (web-safe stack).
- Iconography: minimal, line-based.

Animations
- Subtle fade-and-rise on section reveal (IntersectionObserver + CSS transitions).
- Gentle hover lift and shadow on cards.
- Respect prefers-reduced-motion: reduce/disable animations when set.

Responsive
- Mobile-first layout. Breakpoints: 480px, 768px, 1024px, 1280px.
- Navigation collapses to a menu on narrow screens.

Accessibility
- Color contrast AA minimum.
- Focus states clearly visible.
- Semantic HTML elements, ARIA labels for media player controls.

## 8) Architecture & Tech Stack

- Backend: Python 3.11+, Flask, Jinja2.
- ORM/DB: SQLAlchemy with SQLite (dev/temporary), migration-ready (Alembic).
- Templates: Jinja with includes and occasional macros. Avoid overuse of macros; prefer includes for sections.
- Static assets: CSS and JS in `src/static/` (separate from HTML). Use `main.css` and a small `main.js` for interactions.
- Project structure (current aligns with this):
  - `src/templates/` for pages and partials
  - `src/static/css/`, `src/static/js/`, `src/static/img/`
  - `src/controllers/routes.py` for Flask routes
  - `src/models/` for SQLAlchemy models
  - `server.py`/`run.py` for app bootstrap

## 9) Jinja Conventions & Components

Templates
- Base layouts: `templates/bases/public.html` and `templates/bases/private.html`.
- Components (includes):
  - `templates/public/public_components/header.html`
  - `templates/public/public_components/footer.html`
  - `templates/public/public_components/hero.html`
  - `templates/public/public_components/featured_stories.html`
  - `templates/public/public_components/featured_testimonials.html`
  - `templates/public/public_components/featured_music.html`
  - `templates/public/public_components/subscribe_cta.html`
- Landing page: `templates/public/landing/index.html` uses `{% include %}` for sections.

Macros (use sparingly)
- For repeated small UI units (e.g., `card`, `tag_pill`, `audio_player`). Place macros in `templates/macros/ui.html`.

## 10) Data Model (SQLAlchemy)

Core tables with indicative fields (types to be finalized in implementation):
- Story(id, title, slug, summary, body, author_name, cover_image, created_at, published_at, is_published)
- Testimonial(id, title, slug, quote, body, person_name, location, cover_image, created_at, published_at, is_published)
- MusicTrack(id, title, slug, artist_name, description, audio_url, cover_image, duration_sec, created_at, published_at, is_published)
- Tag(id, name, slug)
- story_tags, testimonial_tags, music_tags (association tables)
- Subscriber(id, email, name, status, unsubscribe_token, created_at, confirmed_at, unsubscribed_at)
- NewsletterIssue(id, subject, body_html, body_text, created_at, updated_at, sent_at)

Migrations via Alembic for schema evolution.

## 11) Routes & URL Structure (MVP)

Public
- GET `/` — Landing (sections via includes)
- GET `/stories` — List stories (paginated)
- GET `/stories/<slug>` — Story detail
- GET `/testimonials` — List testimonials (paginated)
- GET `/testimonials/<slug>` — Testimonial detail
- GET `/music` — List tracks (with audio player)
- GET `/music/<slug>` — Track detail (optional in MVP)
- GET `/subscribe` — Subscribe form
- POST `/subscribe` — Handle subscribe
- GET `/unsubscribe/<token>` — Unsubscribe
- GET `/search` — Query across titles/summaries

Admin (minimal)
- GET `/admin` — Dashboard (auth required)
- CRUD for stories, testimonials, music: `/admin/stories`, `/admin/testimonials`, `/admin/music`
- Newsletter: `/admin/newsletters` (create, preview, send)

## 12) Newsletter Delivery

- Provider abstraction:
  - MVP: SMTP (config via environment variables). Dev mode writes .eml files to disk instead of sending.
  - Future: SendGrid/Mailchimp/Brevo integration.
- Unsubscribe: one-click via unique token; update status to `unsubscribed`.
- Compliance: include physical address placeholder and unsubscribe in footer (admin-configurable).

## 13) Security & Privacy

- CSRF protection for forms.
- Basic auth for admin (env-configured credentials) or Flask-Login.
- Rate limit subscribe endpoint to deter abuse.
- Input validation and safe rendering (sanitize/escape where applicable).
- Secrets/config via `.env` (never committed).

## 14) SEO & Analytics

- SEO: unique titles, meta description, OpenGraph/Twitter cards, sitemap.xml, robots.txt.
- Image `alt` text and structured data for articles (future).
- Optional analytics (GA4 or Plausible). If enabled, provide cookie banner config.

## 15) Performance

- Optimize images; serve modern formats when possible.
- Lazy-load offscreen images.
- Cache headers for static assets.
- Minify/concat CSS/JS (lightweight build step optional; MVP can inline minimal critical CSS or use a single `main.css`).

## 16) Testing & Quality

- Unit tests for models and routes (happy path + edge cases).
- Basic template rendering tests.
- Simple integration test for subscribe/unsubscribe flow.

## 17) Acceptance Criteria (MVP)

Landing
- Renders hero, featured stories/testimonials/music, and subscribe CTA via Jinja includes.
- Subtle animations present and disabled when `prefers-reduced-motion` is on.

Stories & Testimonials
- Listing pages paginate; each card links to detail.
- Detail pages show title, date, tags, and content; share meta present.

Music
- Listing displays tracks with cover art and accessible audio player.

Subscribe/Unsubscribe
- Form accepts valid emails; persists Subscriber with status `active` (or `pending` if double opt-in later).
- Unsubscribe link updates status to `unsubscribed` and confirms to user.

Admin
- Auth-protected minimal UI to create/publish stories, testimonials, and music.
- Can compose a newsletter and send (SMTP or dev .eml output).

Tech
- Uses SQLite via SQLAlchemy.
- CSS/JS are separate files in `src/static/`.
- Jinja includes/macros used appropriately; landing sections are separate includes.
- Site is responsive and accessible (AA contrast, focus states).

## 18) Milestones

M1 — Foundations (routing, base templates, styles, models) — 3–5 days
- Flask app skeleton, base layouts, header/footer components, styles (glassmorphism, responsive grid), models/migrations.

M2 — Content & Pages — 3–5 days
- Stories/testimonials/music pages and detail, admin CRUD (minimal), file/audio handling.

M3 — Subscribe & Newsletter — 2–4 days
- Subscribe form, unsubscribe flow, admin newsletter compose/send (SMTP/dev mode).

M4 — Polish — 2–3 days
- Animations, SEO, accessibility sweeps, performance tuning, tests.

## 19) Risks & Mitigations

- Email deliverability: start with SMTP; plan provider integration later.
- Media hosting: for MVP, store audio as files/URLs; consider CDN later.
- Admin scope creep: keep minimal; plan enhancements post-MVP.

## 20) Open Questions

1) Branding: Do you have a logo, preferred typefaces, and a color palette to lock down? Any reference sites/images you love?
2) Newsletter cadence and sender details: From name/email, physical mailing address for footer (compliance), and preferred provider (if any)?
3) Double opt-in: Should we require confirmation emails at launch, or add later?
4) Content migration: Do you have initial stories/testimonials/music ready? In what format (Docs, Markdown, audio files)?
5) Admin access: Prefer simple env-based basic auth or a login page (Flask-Login) with a stored admin user?
6) Music hosting: Will audio be self-hosted files or embedded from a platform (e.g., SoundCloud/YouTube)?
7) Search: Is a basic title/summary search sufficient for MVP?
8) Analytics: Do you want analytics at launch? If yes, which provider?

---

Implementation notes map to current repo structure (`src/templates`, `src/static`, `src/controllers`, `src/models`). The next step after confirming open questions is to scaffold models, routes, base templates, and landing components per the above.