# Wildlife Sighting Platform

A Flask-based web application that allows users to report sightings of gliders (or other wildlife), securely store data, and view previously submitted reports.  
This project demonstrates full-stack web development with authentication, file uploads, geolocation, and database integration. It can be adapted for citizen science, wildlife monitoring, or environmental education.

---

## Features
- User authentication with signup, login, and logout
- Secure password storage with hashing (Werkzeug)
- Wildlife sighting reporting form with validation
- File upload support for images and videos
- Automatic geolocation lookup using SQLite postcode database
- Database storage of sightings (SQLite)
- Paginated sightings viewer (5 per page, newest first)
- Media type detection and proper file handling
- Static info pages: About, Team, Contact

---

## Screenshots
*(Replace the image links below with your actual screenshots — store them in `/static/screenshots` or link externally.)*

### Login Page
<img width="1837" height="547" alt="login" src="https://github.com/user-attachments/assets/798fdf78-04ea-4023-a761-4e6f83a9316d" />


### Sighting Report Form


### Sightings Viewer


---

## Tech Stack
- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, Jinja2 templates
- **Database:** SQLite (users.db, sightings.db)
- **Authentication:** Werkzeug security (hashed passwords, sessions)
- **Media Handling:** File uploads stored in `/static/uploads/`
- **Geolocation:** SQLite postcode lookup
- **Pagination:** Flask server-side logic

---
