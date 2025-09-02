from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os

# Initialize Flask app
app = Flask(__name__)

# Secret key required for using sessions and flashing messages
app.secret_key = 'your_secret_key'

# Define the upload folder path for storing user-uploaded media
UPLOAD_FOLDER = 'static/uploads'

# Create the uploads directory if it doesn't already exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Create the users database and users table if it doesn't already exist
if not os.path.exists('users.db'):
    with sqlite3.connect('users.db') as conn:
        conn.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  # Auto-incrementing user ID
                firstname TEXT NOT NULL,              # User's first name
                lastname TEXT NOT NULL,               # User's last name
                username TEXT NOT NULL UNIQUE,        # Unique username
                email TEXT NOT NULL UNIQUE,           # Unique email address
                password TEXT NOT NULL UNIQUE         # Unique password (not secure — should be hashed in real apps)
            );
        ''')

# Create the sightings database and sightings table if it doesn't already exist
if not os.path.exists('sightings.db'):
    with sqlite3.connect('sightings.db') as conn:
        conn.execute('''
            CREATE TABLE sightings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  # Unique ID for each sighting
                fname TEXT NOT NULL,                  # First name of person reporting
                lname TEXT,                           # Last name (optional)
                email TEXT NOT NULL,                  # Email of reporter
                description TEXT,                     # Description of the glider sighting
                date TEXT,                            # Date of sighting
                time TEXT,                            # Time of sighting
                address TEXT,                         # Address where glider was seen
                latitude TEXT,                        # Auto-filled latitude from au_postcodes
                longitude TEXT,                       # Auto-filled longitude from au_postcodes
                postcode TEXT,                        # Postcode of sighting location
                country TEXT,                         # Country where sighting occurred
                location TEXT,                        # Place name or suburb
                file BLOB                             # Uploaded image or video of the glider
            );
        ''')
# === Signup Page Route ===
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Handle form submission
    if request.method == 'POST':
        # Retrieve form data
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('signup'))

        # Connect to the users database
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            try:
                # Try inserting the new user into the users table
                cursor.execute('''
                    INSERT INTO users (firstname, lastname, username, email, password)
                    VALUES (?, ?, ?, ?, ?)
                ''', (firstname, lastname, username, email, password))
                conn.commit()

                # Notify and redirect to login on success
                flash('Signup successful! Please log in.')
                return redirect(url_for('login'))

            except sqlite3.IntegrityError:
                # Handles duplicate username/email/password due to UNIQUE constraint
                flash('Username, email, or password already exists!')
                return redirect(url_for('signup'))

    # Show the signup form if GET request
    return render_template('signup.html')


# === Login Page Route ===
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve form input
        username = request.form['username']
        password = request.form['password']

        # Connect to the users database
        with sqlite3.connect('users.db') as conn:
            conn.row_factory = sqlite3.Row  # Enables dictionary-style access to results
            cursor = conn.cursor()

            # Query to check if username and password match
            cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
            user = cursor.fetchone()

            if user:
                # Store user info in session (used for login tracking)
                session['username'] = user['username']
                session['email'] = user['email']
                session['firstname'] = user['firstname']
                session['lastname'] = user['lastname']

                flash('Login successful!')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password!')
                return redirect(url_for('login'))

    # Show login page for GET request
    return render_template('login.html')


# === Logout Route ===
@app.route('/logout')
def logout():
    # Remove username from session to log user out
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))


# === Home Page Route ===
@app.route('/')
def index():
    return render_template('index.html')  # Loads the homepage


# === Report Page Route ===
@app.route('/report', methods=['GET', 'POST'])
def report():
    return render_template('report.html')  # Loads the form for submitting glider sightings

# === Handle Report Sighting Form Submission ===
@app.route('/report_sighting', methods=['POST'])
def report_sighting():
    # Ensure user is logged in before allowing a report
    if 'email' not in session:
        flash('Please login to report a sighting.')
        return redirect(url_for('login'))

    # === Collect form data ===
    fname = request.form['fname']
    lname = request.form.get('lname', '')
    email = request.form['email']
    description = request.form.get('description', '')
    date = request.form.get('date', '')
    time_ = request.form.get('time', '')
    address = request.form.get('address', '')
    postcode = request.form.get('postcode', '').strip()
    location = request.form.get('location', '').strip()
    country = request.form.get('country', '')
    file = request.files['file']
    file_data = file.read()  # Read binary content of uploaded image/video

    # === Try to get latitude and longitude from au_postcodes ===
    with sqlite3.connect('sightings.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Match both location and postcode case-insensitively
        cursor.execute(
            '''SELECT latitude, longitude FROM au_postcodes WHERE LOWER(place_name) = LOWER(?) AND postcode = ?''',
            (location, postcode)
        )
        result = cursor.fetchone()

        if result:
            # If match found, extract latitude and longitude
            latitude = result['latitude']
            longitude = result['longitude']

            # Insert full sighting data into the database
            cursor.execute('''
                INSERT INTO sightings
                (fname, lname, email, description, date, time, address, latitude, longitude, postcode, location, country, file)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (fname, lname, email, description, date, time_, address, latitude, longitude, postcode, location, country, file_data))

            conn.commit()
            flash('Sighting reported successfully!')
            return redirect(url_for('index'))
        else:
            # If no matching postcode-location combo found
            flash('Invalid postcode or location. Please double-check your input.')
            return redirect(url_for('report'))


# === View Sightings Page for Logged-in User ===
@app.route('/sightings', methods=['GET'])
def sightings():
    # Ensure only logged-in users can access their sightings
    if 'username' not in session:
        flash('Please login to view your sightings.')
        return redirect(url_for('login'))

    # === Page logic ===
    page = request.args.get('page', 1, type=int)
    per_page = 5
    offset = (page - 1) * per_page

    with sqlite3.connect('sightings.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Count total sightings for the logged-in user's email
        cursor.execute('SELECT COUNT(*) FROM sightings WHERE email = ?', (session['email'],))
        total_sightings = cursor.fetchone()[0]
        total_pages = (total_sightings + per_page - 1) // per_page  # Calculate total pages

        # Fetch user's sightings (latest first)
        cursor.execute('''
            SELECT * FROM sightings
            WHERE email = ?
            ORDER BY id DESC
            LIMIT ? OFFSET ?
        ''', (session['email'], per_page, offset))

        rows = cursor.fetchall()

        # === Prepare sightings list with media filenames ===
        sightings = []
        for row in rows:
            filename = None
            if row['file']:
                # Determine file type by inspecting content header
                file_extension = '.jpg'
                try:
                    header = row['file'][:20].decode(errors='ignore').lower()
                    if 'jpeg' in header:
                        file_extension = '.jpg'
                    elif 'png' in header:
                        file_extension = '.png'
                    elif 'mp4' in header:
                        file_extension = '.mp4'
                    elif 'webm' in header:
                        file_extension = '.webm'
                    elif 'ogg' in header:
                        file_extension = '.ogg'
                except:
                    pass

                # Name the file uniquely by its sighting ID
                filename = f"{row['id']}_uploaded{file_extension}"
                filepath = os.path.join(UPLOAD_FOLDER, filename)

                # Save file only if it hasn't already been saved
                if not os.path.exists(filepath):
                    with open(filepath, 'wb') as f:
                        f.write(row['file'])

            # Append all relevant data to sightings list
            sightings.append({
                'id': row['id'],
                'fname': row['fname'],
                'lname': row['lname'],
                'email': row['email'],
                'description': row['description'],
                'date': row['date'],
                'time': row['time'],
                'address': row['address'],
                'latitude': row['latitude'],
                'longitude': row['longitude'],
                'postcode': row['postcode'],
                'location': row['location'],
                'country': row['country'],
                'file_path': f"uploads/{filename}" if filename else None
            })

    # Render the sightings template with the user's paginated sightings
    return render_template('sightings.html', sightings=sightings, page=page, total_pages=total_pages)


# Placeholder Pages
@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    # For now just flash a message, later you can save contact form data
    flash('Thank you for contacting us! We will get back to you soon.')
    return redirect(url_for('contact'))

if __name__ == '__main__':
    app.run(debug=True)
