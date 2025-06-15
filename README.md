# Group Availability Scheduler

## Features
- User authentication (registration, login, secure session management)
- Group creation and join via codes
- Availability scheduling and updates
- Automatic overlapping time slot calculation
- Clean UI for merged intervals

## Setup and Installation
```bash
git clone https://github.com/your-username/group-availability-scheduler.git
cd availability
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install flask flask-sqlalchemy intervaltree
python app.py
```

## Usage
- Register/Login
- Create or join a group using a code
- Add availability slots
- View group common time slots

## Additional Information
- Tech Stack: Flask, SQLite, SQLAlchemy, intervaltree
- Security: Passwords not hashed — use hashing in production
