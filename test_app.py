import unittest
from app import app, get_parking_data, get_db_connection

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    #     self.reset_parking_data()  # Reset parking slots to initial state

    # def reset_parking_data(self):
    #     # Manually reset the state of parking slots to avoid test contamination
    #     conn = get_db_connection()
    #     cur = conn.cursor()
    #     cur.execute("UPDATE parking_lots SET status = TRUE")  # Reset all slots to available
    #     conn.commit()
    #     cur.close()
    #     conn.close()

    def test_get_parking_data(self):
        # Call the function to test
        result = get_parking_data()
        print(result)
        
        # Assertions to verify the behavior
        self.assertIsInstance(result, dict)
        self.assertGreater(len(result), 0)
        first_key = next(iter(result))
        self.assertIsInstance(result[first_key], bool)

    def test_index_page(self):
        # Send a GET request to the index page
        response = self.app.get('/')
        
        # Assertions to verify the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)  # Adjusted to check for login page

    def test_book_slot(self):
        # Send a POST request to book a slot
        response = self.app.post('/book', data=dict(slot='A1'))
        
        # Assertions to verify the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Slot A1 successfully booked!', response.data)

    def test_release_slot(self):
        # Send a POST request to release a slot
        self.app.post('/book',data=dict(slot='A1'))
        response = self.app.post('/release', data=dict(slot='A1'))
        
        # Assertions to verify the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Slot A1 has been released.', response.data)  # Adjusted to match actual message
    
    def test_signup(self):
        # Send a POST request to signup
        response = self.app.post('/signup', data=dict(new_user_id='newuser', new_password='newpassword'))
        # print(response.data)
        # print()

        # Assertions to verify the signup response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New user created successfully', response.data)  # Adjusted to check for success message

        # Clean up the newly created user entry
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE name = %s;", ('newuser',))
        conn.commit()
        cur.close()
        conn.close()

    def test_signup_user_exists(self):
        # Send a POST request to signup with an existing user
        response = self.app.post('/signup', data=dict(new_user_id='existinguser', new_password='password'))
        
        # Assertions to verify the signup failure response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User already exists', response.data)  # Adjusted to check for error message

    def test_login_and_home_page(self):
        # Send a POST request to login
        response = self.app.post('/login', data=dict(user_id='software1', password='shrulep1'))
        
        # Assertions to verify the login response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Smart Parking System', response.data)  # Adjusted to check for home page content

    def test_login_fail(self):
        # Send a POST request to login with invalid credentials
        response = self.app.post('/login', data=dict(user_id='invaliduser', password='invalidpassword'))
        
        # Assertions to verify the login failure response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid login credentials.', response.data)  # Adjusted to check for error message
    

    def test_add_to_queue(self):
        # Send a POST request to add to queue
        response = self.app.post('/add_to_queue', data=dict(user_id='testuser'))
        
        # Assertions to verify the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been added to the waiting queue.', response.data)  # Adjusted to match actual message

    def test_remove_from_queue(self):
        # Send a POST request to remove from queue
        response = self.app.post('/remove_from_queue', data=dict(user_id='testuser'))
        
        # Assertions to verify the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been removed from the waiting queue.', response.data)  # Adjusted to match actual message
    
    def test_release_nonexistent_slot(self):
        # Send a POST request to release a nonexistent slot
        response = self.app.post('/release', data=dict(slot='Z9'))
        
        # Assertions to verify the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Error: Slot &#39;Z9&#39; does not exist.", response.data)  # Adjusted to match actual message

    def test_queue_notification_on_slot_release(self):
        # Add a user to the waiting queue
        self.app.post('/book',data=dict(slot='A1'))
        self.app.post('/book',data=dict(slot='A2'))
        self.app.post('/book',data=dict(slot='B1'))
        self.app.post('/book',data=dict(slot='B2'))
        
        self.app.post('/add_to_queue', data=dict(user_id='queueuser2'))
        # Release a slot by another user
        self.app.post('/release', data=dict(slot='A1'))
        response= self.app.post('/login',data=dict(user_id='software1', password='shrulep1'))
        # Assertions to verify the queue notification
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'A parking slot is now available! Book it quickly.', response.data)  # Check for the notification message
        


    # booking an already booked slot
    def test_booking_already_booked_slot(self):
        # Book a slot
        self.app.post('/book', data=dict(slot='A1'))
        # Try to book the same slot again
        response = self.app.post('/book', data=dict(slot='A1'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Slot A1 is already occupied.', response.data)


    # releasing a free slot
    def test_releasing_free_slot(self):
    # Try to release a slot that is already free
        self.app.post('/release', data=dict(slot='A1'))

        response = self.app.post('/release', data=dict(slot='A1'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Slot A1 is already available.', response.data)



    # concurrent accesss



    
if __name__ == '__main__':
    unittest.main()