# Debate Forum Web Application

A structured debate platform built with Flask and SQLite that enables users to engage in organised discussions through topics, claims, and hierarchical replies. The application implements a sophisticated argument structure with relationship types.

This project was built to understand full-stack web development, database schema design for complex relationships, and creating interactive user experiences with proper authentication and session management.

## 📦 Technologies & Concepts

- `Python / Flask`
- `SQLite`
- `Session-based authentication`
- `RESTful API design`
- `Responsive HTML/CSS/JavaScript`
- `AJAX requests`
- `Database schema design`
- `SQL injection prevention`
- `Form validation`

## 🥀 Features
### ▶ User Authentication System
- User registration with username/password
- Secure login/logout functionality
- Session persistence across page reloads
- Protected routes requiring authentication
- User tracking for all content creation

### ▶ Topic Management
- Browse all available debate topics
- Create new topics (requires login)
- Default topics auto-populated on first run
- Topics display creation time and author
- Dynamic topic list with real-time updates

### ▶ Claim System
- Post claims under specific topics
- View all claims for a topic
- Claims sorted by creation time
- Each claim shows author and timestamp
- Claim relationships (Opposed/Equivalent) (schema-ready)
- Link claims to create debate structures

### ▶ Reply Hierarchy
Multiple reply types with semantic meaning:
- Replies to Claims:
  - Clarification — request or provide clarity
  - Supporting Argument — evidence supporting the claim
  - Counter Argument — evidence opposing the claim
- Replies to Replies:
  - Evidence — factual support
  - Support — agreement or reinforcement
  - Rebuttal — counterpoint or disagreement

### ▶ Database Architecture
Complex relational schema featuring:
- User management with admin support
- Topic tracking with update timestamps
- Claim-to-claim relationships (many-to-many)
- Separate reply text storage for reusability
- Typed relationships between entities
- Cascading deletes and updates
- Foreign key constraints
- Automatic timestamp tracking

### ▶ Interactive UI
- Modal popups for all forms
- Real-time form validation
- Dynamic content loading without page refresh
- Responsive design
- Clean, accessible interface
- Visual feedback for user actions

### ▶ Security Features
- Session-based authentication
- Parameterized SQL queries (prevents injection)
- Server-side input validation
- Login checks for protected actions
- Proper error handling and user feedback

## 🤨 How It Was Built
1- Database Design — Created normalized schema with complex relationships

2- Flask Backend — Built RESTful routes for all CRUD operations

3- Authentication System — Implemented session management and login protection

4- Topic & Claim CRUD — Created endpoints for content creation and retrieval

5- Reply System — Built hierarchical reply structure with typed relationships

6- Frontend Interface — Designed responsive UI with modal forms

7- AJAX Integration — Connected frontend to backend without page reloads

8- Data Validation — Added client and server-side validation

9- SQL Optimisation — Used JOINs and proper indexing via foreign keys

## 🤓☝️ What I Learned
### Database Design
- Designing schemas for complex many-to-many relationships
- Using junction tables for typed relationships
- Implementing cascading constraints
- Understanding when to use foreign keys vs raw IDs
- Separating concerns (reply text vs reply relationships)

### Backend Development
- Building RESTful APIs with Flask
- Session management and user authentication
- Transaction handling in SQLite
- Proper error responses and status codes
- SQL injection prevention techniques

### Frontend Integration
- AJAX requests for dynamic updates
- Form handling without page reloads
- Modal UI patterns
- Client-side validation
- DOM manipulation with vanilla JavaScript

### Full-Stack Architecture
- Separating presentation from business logic
- Template inheritance with Jinja2
- Static file management
- Request/response cycle
- State management across client and server

### Web Security
- Session security basics
- Input sanitization
- SQL injection prevention
- Authentication vs Authorisation
- Secure password handling considerations

## Running the Project
`# Install dependencies`

`pip install flask`

`# Initialize the database`

`sqlite3 debate.sqlite < 5013dbinit.sql`

`# Run the application`

`python app.py`

`# Access at http://localhost:5000`

## Things to Consider
- Passwords are currently stored as plain text
- Reply-to-reply functionality is implemented in the backend but not fully displayed in the UI
- The application uses SQLite's Julian time format for timestamps
- Foreign key support must be explicitly enabled in SQLite
