---
applyTo: '**'
---
# Product Requirements Document (PRD) Instructions
# Product Requirements Document (PRD)

## Project Title:
A Place For Me

---

## Project Overview:
"A Place For Me" is a digital platform designed to empower and uplift individuals by sharing faith-based content. The application allows the client to post blogs, upload God stories, share songs, post testimonials, manage subscribers, release newsletters, and upload radio sessions. The goal is to create a welcoming, interactive, and inspiring online space where the community can engage, share, and grow together in faith.

---

## Level:
Easy to Medium

---

## Type of Project:
Content Management System (CMS), Blogging Platform, Community Engagement

---

## Tech Stack & Skills Required:
- **Backend:** Python (Flask), Flask-Bcrypt (for password hashing), Flask-Mail (for emails), Flask-Login (for session/auth), Flask-Uploads or direct file handling
- **Frontend:** HTML, CSS, JavaScript, Jinja2 templates (Flask rendering)
- **Database:** SQLite (local), SQLAlchemy (ORM)
- **File Storage:** 
  - Local filesystem for development (`/uploads` or `/media`)
  - Optionally, Cloudinary free tier for dev/test deployments (supports images, audio, video)
- **Authentication & Subscription:** Flask-Login, Flask-Bcrypt
- **MVC Structure:** Separation of models, views, controllers (Flask Blueprints recommended)
- **Testing:** pytest, Flask-Testing

---

## Frontend Framework Guidelines

### Component-Based Architecture with Jinja2
- **Component Philosophy:** Build reusable UI components using Jinja2 templates to maintain DRY principles and ensure consistency across the application.
- **Jinja Macros:** Create Jinja macros for any component used in multiple places (e.g., navigation bars, forms, cards, buttons, modals).
- **Template Inheritance:** Use template inheritance with base templates for different layouts (admin, public, auth).

### File Organization & Separation of Concerns
- **Templates Structure:**
  - `/templates/bases/` - Base templates and layouts
  - `/templates/components/` - Reusable Jinja macros and components
  - `/templates/pages/` - Page-specific templates
  - `/templates/forms/` - Form-specific templates and macros
- **Static Assets:**
  - `/static/css/` - All CSS stylesheets (component-specific and global)
  - `/static/js/` - All JavaScript files (component-specific and global)
  - `/static/images/` - Image assets
  - `/static/icons/` - Icon assets

### CSS Architecture
- **Global Styles:** `main.css` for base styles, typography, and color variables
- **Component Styles:** Individual CSS files for complex components (e.g., `navigation.css`, `card.css`)
- **Utility Classes:** Small utility classes for spacing, colors, and common patterns
- **CSS Variables:** Use CSS custom properties for the nature-inspired color palette and consistent spacing
- **Responsive Design:** Mobile-first approach with clean breakpoints

### JavaScript Organization
- **Modular JS:** Separate JavaScript files for different functionality areas
- **Component-Specific JS:** Individual JS files for interactive components
- **Global JS:** `main.js` for site-wide functionality and utilities
- **Progressive Enhancement:** Ensure core functionality works without JavaScript

### Component Guidelines
- **Reusable Macros:** Create macros for:
  - Navigation components
  - Form elements (input fields, buttons, validation messages)
  - Content cards (blog posts, stories, testimonials)
  - Media players (audio, video)
  - Admin table components
  - Pagination components
  - Alert/notification components
- **Macro Parameters:** Design macros with flexible parameters for customization
- **Documentation:** Comment macros with usage examples and parameter descriptions

### Design System Integration
- **Nature-Inspired Theme:** Implement the forest green color palette (#228B22, #8A9A5B, #32CD32)
- **Typography System:** Clean sans-serif fonts with consistent sizing hierarchy
- **Component Library:** Build a cohesive set of UI components following the styling guide
- **Accessibility:** Ensure all components meet WCAG guidelines with proper contrast and semantics

### Development Standards
- **Template Naming:** Use clear, descriptive names for templates and macros
- **CSS Methodology:** Follow BEM or similar methodology for CSS class naming
- **JavaScript Standards:** Use modern ES6+ features with graceful degradation
- **Performance:** Optimize asset loading and minimize HTTP requests
- **Testing:** Include frontend testing for critical interactive components

---

## Key Features & Milestones

### Milestone 1: User Authentication & Admin Panel Foundation
- **User Registration & Login:**  
  - Secure sign-up/sign-in system with hashed passwords using Flask-Bcrypt.
  - Role-based access (admin and regular user).
  - Session management via Flask-Login.
- **Admin Panel:**  
  - Admin dashboard for content management and moderation.
  - Access restricted to authenticated admin users.

### Milestone 2: Core Content Management
- **Blog Posting:**  
  - Admin can create, edit, delete, and publish blog posts (rich text via Markdown or WYSIWYG editor).
  - Posts displayed in reverse chronological order.
- **God Stories Submission:**  
  - Admin can upload and organize faith or God-centered stories with support for text, audio, or video.
- **Songs Upload:**  
  - Audio file upload and categorization, with in-browser streaming.
- **Testimonials:**  
  - Admin can post and manage user testimonials or personal testimonies.

### Milestone 3: Subscriber & Community Engagement
- **Subscriber Management:**  
  - Users can subscribe with email to updates.
  - Admin can view, manage, and export subscriber lists; basic analytics (number, growth).
- **Newsletter Release:**  
  - Compose and send newsletters to subscribers (Flask-Mail).
  - Templates for newsletters using Jinja.

### Milestone 4: Advanced Content Engagement
- **Radio Sessions Upload:**  
  - Admin can upload and archive radio sessions as audio files or podcasts.
- **Commenting & Engagement:**  
  - Optional: Allow users to comment on posts (with moderation).
- **Notifications:**  
  - Notify subscribers via email for new content (optional toggle).

---

## Application Architecture

- **MVC Structure:**
  - **Models:** SQLAlchemy models for Users, Posts, Stories, Songs, Testimonials, Subscribers, Newsletters, Radio Sessions.
  - **Views:** Jinja2 HTML templates with component-based architecture and macro system.
  - **Controllers:** Flask Blueprints for organized routing and controller logic per feature.

- **Frontend Architecture:**
  - **Template Hierarchy:** Base templates with inheritance for consistent layouts
  - **Component System:** Reusable Jinja macros for common UI elements
  - **Asset Organization:** Separated CSS and JavaScript files by functionality
  - **Responsive Design:** Mobile-first approach with clean grid system
  - **Progressive Enhancement:** Core functionality works without JavaScript

- **Component Structure:**
  ```
  /templates/
    ├── bases/           # Layout templates
    ├── components/      # Reusable Jinja macros
    ├── pages/          # Feature-specific pages
    └── forms/          # Form templates and macros
  
  /static/
    ├── css/            # Stylesheets (global and component-specific)
    ├── js/             # JavaScript files (global and component-specific)
    ├── images/         # Image assets
    └── icons/          # Icon assets
  ```

- **Security:**
  - Passwords hashed with Flask-Bcrypt.
  - User sessions securely managed with Flask-Login.
  - CSRF protection enabled.

- **Database:**
  - SQLite for development; models abstracted for easy migration.

- **File Uploads:**
  - Media files (audio, images, video) stored in `/uploads` or `/media` directory during development.
  - Optionally, Cloudinary free tier can be used for development and test deployments for broader access and easier sharing.
  - File validation and size limits enforced.

---

## Client Information:
The client is a faith-driven content creator dedicated to inspiring, uplifting, and connecting people through stories, music, and shared experiences. Her platform aims to foster a supportive community, encourage personal growth, and spread positivity rooted in faith.

---

## Stretch Features (Future Considerations)
- Mobile app version (iOS/Android, API endpoints)
- Event calendar for live sessions
- Donation or support feature
- Social media sharing integration
- Podcast distribution to external platforms
- Admin analytics dashboard

---

## Success Metrics:
- User engagement (number of posts, stories, and songs uploaded)
- Subscriber growth
- Newsletter open and click rates
- Community feedback and testimonials

---