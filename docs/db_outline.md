# Concise Database Table Design Questions (Prefilled for "A Place For Me")

For each table, quickly answer:

---

## users

1. **Purpose:**  
   Store user accounts (admin, subscribers, regular users, and authors created by admin).

2. **Key Fields:**  
   - Required: id (PK), username, email, password_hash, role, created_at  
   - Optional: last_login, is_managed (True if admin-created on behalf of author, False if self-created)  
   - PK: id

3. **Relationships:**  
   - May relate to blog posts, god stories, comments (authorship)

4. **Usage:**  
   - Admin: manage content, create authors  
   - User: register, login, subscribe, comment  
   - Authors: accounts may be admin-managed; do not require direct login

5. **Security:**  
   - Stores password hashes (bcrypt)  
   - Email is sensitive

6. **Metadata:**  
   - created_at, last_login, is_managed

---

## blog_posts

1. **Purpose:**  
   Store blog posts created by admin; support draft/publish modes and scheduling.

2. **Key Fields:**  
   - Required: id (PK), title, content, author_id (FK), created_at  
   - Optional: image_path, updated_at, status (draft/published), publish_at (datetime), is_published  
   - PK: id

3. **Relationships:**  
   - author_id references users(id)

4. **Usage:**  
   - Admin creates/edits; users view (and possibly comment)
   - Supports rich text and scheduling for future publication

5. **Security:**  
   - Content not sensitive, but only admin can modify

6. **Metadata:**  
   - created_at, updated_at, status, publish_at

---

## god_stories

1. **Purpose:**  
   Store "God stories" (testimonies/faith stories); support draft/publish modes and scheduling.

2. **Key Fields:**  
   - Required: id (PK), title, content, author_id (FK), created_at  
   - Optional: audio_path, video_path, image_path, updated_at, status (draft/published), publish_at (datetime), is_published  
   - PK: id

3. **Relationships:**  
   - author_id references users(id) (can be admin-managed authors)

4. **Usage:**  
   - Admin uploads on behalf of authors; users view/listen
   - Supports scheduling and draft/publish

5. **Security:**  
   - Media files handled with care

6. **Metadata:**  
   - created_at, updated_at, status, publish_at

---

## songs

1. **Purpose:**  
   Store uploaded song info and files; support draft/publish modes and scheduling.

2. **Key Fields:**  
   - Required: id (PK), title, file_path, uploaded_by (FK), created_at  
   - Optional: description, updated_at, status (draft/published), publish_at (datetime), is_published  
   - PK: id

3. **Relationships:**  
   - uploaded_by references users(id) (can be admin or managed author)

4. **Usage:**  
   - Admin uploads; users stream/listen
   - Supports scheduling and draft/publish

5. **Security:**  
   - File paths/media

6. **Metadata:**  
   - created_at, updated_at, status, publish_at

---

## testimonials

1. **Purpose:**  
   Store user or admin-provided testimonials; support draft/publish modes and scheduling.

2. **Key Fields:**  
   - Required: id (PK), content, author_id (FK), created_at  
   - Optional: is_approved, image_path, updated_at, status (draft/published), publish_at (datetime), is_published  
   - PK: id

3. **Relationships:**  
   - author_id references users(id) (can be admin-managed)

4. **Usage:**  
   - Users/admin submit; admin approves, schedules, or drafts

5. **Security:**  
   - Moderation required

6. **Metadata:**  
   - created_at, approved_at, updated_at, status, publish_at

---

## subscribers

1. **Purpose:**  
   Store email subscribers.

2. **Key Fields:**  
   - Required: id (PK), email, subscribed_at  
   - Optional: name  
   - PK: id

3. **Relationships:**  
   - None direct, but may link to users

4. **Usage:**  
   - Users subscribe; admin exports/list

5. **Security:**  
   - Email is sensitive info

6. **Metadata:**  
   - subscribed_at

---

## newsletters

1. **Purpose:**  
   Store sent newsletters; support draft/publish modes and scheduling.

2. **Key Fields:**  
   - Required: id (PK), subject, body, sent_at  
   - Optional: author_id (FK), status (draft/scheduled/sent), scheduled_at  
   - PK: id

3. **Relationships:**  
   - author_id references users(id)

4. **Usage:**  
   - Admin composes/schedules/sends; users receive

5. **Security:**  
   - Content non-sensitive

6. **Metadata:**  
   - sent_at, status, scheduled_at

---

## radio_sessions

1. **Purpose:**  
   Store uploaded radio session files and metadata; support draft/publish modes and scheduling.

2. **Key Fields:**  
   - Required: id (PK), title, file_path, uploaded_by (FK), created_at  
   - Optional: description, updated_at, status (draft/published), publish_at (datetime), is_published  
   - PK: id

3. **Relationships:**  
   - uploaded_by references users(id) (can be admin-managed)

4. **Usage:**  
   - Admin uploads; users stream/listen
   - Supports scheduling and draft/publish

5. **Security:**  
   - File paths/media

6. **Metadata:**  
   - created_at, updated_at, status, publish_at

---

## logbook

1. **Purpose:**  
   Store session tokens for logged-in users.

2. **Key Fields:**  
   - Required: id (PK), user_id (FK), token_hash (hashed user info), created_at, expires_at  
   - Optional: is_active  
   - PK: id

3. **Relationships:**  
   - user_id references users(id)

4. **Usage:**  
   - Token generated on login, stored in session; used to authenticate users on requests.
   - Token validated for expiration and activity.

5. **Security:**  
   - token_hash is securely generated and stored (not reversible)
   - Tied to user_id for traceability
   - Tokens expire for security

6. **Metadata:**  
   - created_at, expires_at, is_active

---

## log_entries

1. **Purpose:**  
   Store application logs for auditing and debugging (custom logger output).

2. **Key Fields:**  
   - Required: id (PK), timestamp, level, message, source  
   - Optional: user_id (FK), session_id, extra_data  
   - PK: id

3. **Relationships:**  
   - user_id references users(id) (optional, if log is associated with a user)

4. **Usage:**  
   - Logger writes entries here; admins may review for errors/auditing.

5. **Security:**  
   - No sensitive data in logs, but should handle privacy for user info

6. **Metadata:**  
   - timestamp, extra_data

---

## comments (optional)

1. **Purpose:**  
   Store comments on posts, stories, etc.

2. **Key Fields:**  
   - Required: id (PK), content, author_id (FK), post_id (FK), created_at  
   - Optional: is_approved  
   - PK: id

3. **Relationships:**  
   - author_id references users(id), post_id references blog_posts(id) or god_stories(id)

4. **Usage:**  
   - Users comment; admin moderates

5. **Security:**  
   - Moderation required

6. **Metadata:**  
   - created_at, approved_at

---