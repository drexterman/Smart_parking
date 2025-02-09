# Smart Parking System

A Flask-based web application for managing a smart parking system with user authentication, real-time slot booking, and queue management.

This project implements a smart parking system that allows users to view available parking slots, book and release slots, and join a waiting queue when all slots are occupied. The system is designed to handle concurrent access and provides real-time updates on parking slot availability.

Key features include:
- User authentication (login and signup)
- Real-time parking slot booking and release
- Waiting queue management for fully occupied parking lots
- Concurrent access handling for booking and releasing slots
- Unit tests to ensure system reliability and functionality

## Repository Structure

```
.
├── app.py
├── loop.py
├── README.md
├── templates
│   ├── index.html
│   └── index1.html
└── test_app.py
```

- `app.py`: Main Flask application file containing route handlers and core functionality
- `test_app.py`: Unit tests for the Flask application
- `loop.py`: Script to run the test suite multiple times
- `templates/`: Directory containing HTML templates for the web interface

## Usage Instructions

### Installation

1. Ensure you have Python 3.7+ installed
2. Clone the repository:
   ```
   git clone <repository-url>
   cd smart-parking-system
   ```
3. Install required dependencies:
   ```
   pip install flask psycopg2
   ```

### Configuration

1. Set up a PostgreSQL database and update the `DB_CONFIG` in `app.py` with your database credentials:

```python
DB_CONFIG = {
    "dbname": "software_eng1",
    "user": "postgres",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}
```

2. Initialize the database with the required tables (users, parking_lots, waiting_queue)

### Running the Application

1. Start the Flask application:
   ```
   python app.py
   ```
2. Access the application in your web browser at `http://localhost:5000`

### Testing

Run the test suite:
```
python test_app.py
```

To run the test suite multiple times:
```
python loop.py
```

### Common Use Cases

1. User Registration:
   - Navigate to the signup page
   - Enter a new username and password
   - Submit the form to create a new account

2. User Login:
   - Enter your username and password on the login page
   - Upon successful login, you'll be redirected to the main parking system interface

3. Booking a Parking Slot:
   - View available parking slots on the main interface
   - Click the "Book" button next to an available slot to reserve it

4. Releasing a Parking Slot:
   - Find your booked slot on the interface
   - Click the "Release" button to make the slot available again

5. Joining the Waiting Queue:
   - If all slots are occupied, click the "Join Queue" button
   - You'll be notified when a slot becomes available

### Troubleshooting

1. Database Connection Issues:
   - Ensure PostgreSQL is running and accessible
   - Verify the database credentials in `DB_CONFIG`
   - Check for any firewall restrictions on the database port

2. Concurrent Access Errors:
   - The system uses database transactions to handle concurrency
   - If you encounter unexpected behavior, check the application logs for detailed error messages

3. Test Failures:
   - Ensure the database is properly initialized with test data
   - Verify that all required tables (users, parking_lots, waiting_queue) exist in the database
   - Check for any changes in the database schema that might affect the tests

### Debugging

To enable debug mode and verbose logging:

1. Set `debug=True` in `app.run()` at the end of `app.py`
2. Run the application with:
   ```
   python app.py
   ```
3. Check the console output for detailed logs and error messages

Log files are typically stored in the application's root directory or as specified by your deployment environment.

## Data Flow

The Smart Parking System follows this general data flow for user interactions:

1. User Authentication:
   Client -> Login/Signup Request -> Server -> Database Verification -> Response to Client

2. Parking Slot Management:
   Client -> Book/Release Request -> Server -> Database Update -> Notification to Waiting Users -> Response to Client

3. Queue Management:
   Client -> Join/Leave Queue Request -> Server -> Database Update -> Response to Client

```
+--------+    HTTP     +--------+    SQL     +----------+
| Client | <---------> | Server | <---------> | Database |
+--------+   Requests  +--------+   Queries  +----------+
    ^                      |
    |                      |
    |    Notifications     |
    +----------------------+
```

The server acts as an intermediary between the client and the database, handling all business logic and ensuring data consistency. Notifications are sent to clients when parking availability changes or when it's their turn from the waiting queue.