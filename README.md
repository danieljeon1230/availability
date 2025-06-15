# Group Availability Scheduler

A Flask-based web application that helps groups find common available time slots for meetings or events. Users can create groups, join existing groups, and specify their availability to find overlapping time slots with other group members.

## Features

- User Authentication
  - Registration and login system
  - Secure session management
- Group Management
  - Create new groups with unique codes
  - Join existing groups using group codes
  - Leave groups
- Availability Scheduling
  - Add multiple time slots for your availability
  - View common available time slots among group members
  - Update availability for specific groups
- Smart Time Slot Finding
  - Automatically calculates overlapping time slots
  - Handles multiple availability ranges per user
  - Merges overlapping intervals for cleaner results

## Technical Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML Templates
- **Dependencies**:
  - Flask
  - Flask-SQLAlchemy
  - intervaltree (for time slot calculations)

## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/danieljeon1230/availability.git
cd availability
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install flask flask-sqlalchemy intervaltree
```

4. Initialize the database:
```bash
python app.py
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. Register a new account or login with existing credentials
2. Create a new group or join an existing one using a group code
3. Add your availability time slots for specific groups
4. View common available time slots with other group members
5. Update your availability as needed

## Database Schema

The application uses the following models:
- User: Stores user credentials
- Group: Stores group information and unique codes
- Membership: Manages user-group relationships
- Availability: Stores user availability time slots for specific groups

## Security Notes

- The application uses session-based authentication
- Passwords are stored in plain text (consider implementing password hashing for production)
- A secret key is required for session management

## Contributing

Feel free to submit issues and enhancement requests!
