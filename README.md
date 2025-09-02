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

### Signup Page
<img width="1820" height="877" alt="signup" src="https://github.com/user-attachments/assets/f9bc7d9b-727b-4cca-be58-5ee5724c46d4" />


### Sighting Report Form
<img width="1785" height="831" alt="report_sighting" src="https://github.com/user-attachments/assets/663259c8-94ba-4bbf-b0d1-3d48e47c370f" />


### Sightings Viewer
<img width="1513" height="586" alt="sighting_view" src="https://github.com/user-attachments/assets/fe64e9a2-5a93-4f92-8874-eb87c1461deb" />

## Data flow 
### Register Data Flow
<img width="728" height="329" alt="image" src="https://github.com/user-attachments/assets/a5286b38-c7a5-4af7-96b0-98881da68d6d" />

### Login Data Flow
<img width="728" height="419" alt="image" src="https://github.com/user-attachments/assets/4b10de62-0e6c-4016-8274-da1aa5b6d501" />

### Sightings Data Flow
<img width="728" height="419" alt="image" src="https://github.com/user-attachments/assets/60061c26-39b9-4b08-8241-f386393b78e5" />


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
