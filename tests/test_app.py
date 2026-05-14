"""
Test Suite for Student Management System
Tests all CRUD operations and API endpoints

This demonstrates best practices for testing:
- Unit tests for business logic
- Integration tests for database operations
- API endpoint testing
- Error handling validation

Run tests with: pytest
Run tests with coverage: pytest --cov=.
"""

import pytest
import json
import os
from pathlib import Path

# Import the Flask app and StudentManager
from app import app, student_manager
from routes.student_manager import StudentManager

# ==================== PYTEST FIXTURES ====================

@pytest.fixture
def client():
    """
    Flask test client fixture
    Provides a test client for making requests to the Flask app
    """
    # Use test configuration
    app.config['TESTING'] = True
    
    # Create test client
    with app.test_client() as client:
        yield client
    
    # Cleanup: remove test database
    if os.path.exists('students_db.json'):
        os.remove('students_db.json')


@pytest.fixture
def student_mgr():
    """
    StudentManager fixture
    Provides a fresh StudentManager instance for each test
    """
    # Cleanup before test
    if os.path.exists('students_db.json'):
        os.remove('students_db.json')
    
    # Create new manager
    manager = StudentManager()
    
    yield manager
    
    # Cleanup after test
    if os.path.exists('students_db.json'):
        os.remove('students_db.json')


@pytest.fixture
def sample_student():
    """Sample student data for testing"""
    return {
        'name': 'John Doe',
        'email': 'john@example.com',
        'phone': '+1-234-567-8900',
        'grade': 'Junior',
        'major': 'Computer Science'
    }


# ==================== HEALTH CHECK TESTS ====================

class TestHealthCheck:
    """Test health check endpoint"""
    
    def test_health_check_endpoint(self, client):
        """Test that health check endpoint returns 200 OK"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['service'] == 'Student Management System'
        assert 'timestamp' in data
    
    def test_health_check_response_format(self, client):
        """Test health check response has correct format"""
        response = client.get('/health')
        data = json.loads(response.data)
        
        # Check response contains expected keys
        assert 'status' in data
        assert 'timestamp' in data
        assert 'service' in data
        
        # Check status is 'healthy'
        assert data['status'] == 'healthy'


# ==================== STUDENT MANAGER TESTS ====================

class TestStudentManager:
    """Test StudentManager CRUD operations"""
    
    def test_initialization(self, student_mgr):
        """Test StudentManager initializes correctly"""
        assert student_mgr is not None
        assert os.path.exists('students_db.json')
    
    def test_add_student(self, student_mgr, sample_student):
        """Test adding a student"""
        result = student_mgr.add_student(sample_student)
        
        # Check result has expected fields
        assert result is not None
        assert result['name'] == sample_student['name']
        assert result['email'] == sample_student['email']
        assert 'id' in result
        assert result['id'] == 1
    
    def test_add_student_without_name_raises_error(self, student_mgr):
        """Test that adding student without name raises error"""
        student_data = {
            'email': 'test@example.com',
            'phone': '1234567890'
        }
        
        with pytest.raises(ValueError):
            student_mgr.add_student(student_data)
    
    def test_add_student_without_email_raises_error(self, student_mgr):
        """Test that adding student without email raises error"""
        student_data = {
            'name': 'John Doe',
            'phone': '1234567890'
        }
        
        with pytest.raises(ValueError):
            student_mgr.add_student(student_data)
    
    def test_get_all_students_empty(self, student_mgr):
        """Test getting students from empty database"""
        students = student_mgr.get_all_students()
        assert students == []
        assert len(students) == 0
    
    def test_get_all_students(self, student_mgr, sample_student):
        """Test getting all students"""
        # Add multiple students
        student_mgr.add_student(sample_student)
        student_mgr.add_student({
            'name': 'Jane Smith',
            'email': 'jane@example.com',
            'phone': '9876543210'
        })
        
        # Get all students
        students = student_mgr.get_all_students()
        assert len(students) == 2
        assert students[0]['name'] == 'John Doe'
        assert students[1]['name'] == 'Jane Smith'
    
    def test_get_student_by_id(self, student_mgr, sample_student):
        """Test getting a student by ID"""
        # Add student
        added = student_mgr.add_student(sample_student)
        student_id = added['id']
        
        # Get student
        student = student_mgr.get_student_by_id(student_id)
        assert student is not None
        assert student['name'] == sample_student['name']
        assert student['email'] == sample_student['email']
    
    def test_get_student_by_id_not_found(self, student_mgr):
        """Test getting non-existent student returns None"""
        student = student_mgr.get_student_by_id(999)
        assert student is None
    
    def test_update_student(self, student_mgr, sample_student):
        """Test updating a student"""
        # Add student
        added = student_mgr.add_student(sample_student)
        student_id = added['id']
        
        # Update student
        updated_data = {
            'name': 'John Updated',
            'email': 'john.updated@example.com',
            'phone': '+1-111-111-1111',
            'grade': 'Senior',
            'major': 'Information Technology'
        }
        
        result = student_mgr.update_student(student_id, updated_data)
        assert result is not None
        assert result['name'] == 'John Updated'
        assert result['email'] == 'john.updated@example.com'
        assert result['grade'] == 'Senior'
    
    def test_update_student_not_found(self, student_mgr):
        """Test updating non-existent student returns None"""
        result = student_mgr.update_student(999, {'name': 'Test'})
        assert result is None
    
    def test_delete_student(self, student_mgr, sample_student):
        """Test deleting a student"""
        # Add student
        added = student_mgr.add_student(sample_student)
        student_id = added['id']
        
        # Verify student exists
        assert student_mgr.get_student_by_id(student_id) is not None
        
        # Delete student
        result = student_mgr.delete_student(student_id)
        assert result is True
        
        # Verify student is deleted
        assert student_mgr.get_student_by_id(student_id) is None
    
    def test_delete_student_not_found(self, student_mgr):
        """Test deleting non-existent student returns False"""
        result = student_mgr.delete_student(999)
        assert result is False
    
    def test_get_student_count(self, student_mgr, sample_student):
        """Test getting student count"""
        # Add students
        student_mgr.add_student(sample_student)
        student_mgr.add_student({
            'name': 'Another Student',
            'email': 'another@example.com'
        })
        
        # Check count
        count = student_mgr.get_student_count()
        assert count == 2
    
    def test_search_students(self, student_mgr, sample_student):
        """Test searching students by name"""
        # Add students
        student_mgr.add_student(sample_student)
        student_mgr.add_student({
            'name': 'Jane Smith',
            'email': 'jane@example.com'
        })
        
        # Search by name
        results = student_mgr.search_students('john')
        assert len(results) == 1
        assert results[0]['name'] == 'John Doe'
    
    def test_search_students_by_email(self, student_mgr, sample_student):
        """Test searching students by email"""
        student_mgr.add_student(sample_student)
        
        # Search by email
        results = student_mgr.search_students('john@example.com')
        assert len(results) == 1
        assert results[0]['email'] == 'john@example.com'


# ==================== FLASK ROUTES TESTS ====================

class TestFlaskRoutes:
    """Test Flask route handlers"""
    
    def test_dashboard_route(self, client):
        """Test dashboard route returns 200"""
        response = client.get('/dashboard')
        assert response.status_code == 200
        assert b'Dashboard' in response.data or b'Student' in response.data
    
    def test_home_route_redirect(self, client):
        """Test home route (/) works"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_students_route(self, client):
        """Test students list route"""
        response = client.get('/students')
        assert response.status_code == 200
    
    def test_add_student_get(self, client):
        """Test GET request to add student form"""
        response = client.get('/add-student')
        assert response.status_code == 200
        assert b'name' in response.data  # Form should contain name field
    
    def test_add_student_post(self, client, sample_student):
        """Test POST request to add student"""
        response = client.post('/add-student', data=sample_student, follow_redirects=True)
        assert response.status_code == 200
    
    def test_add_student_missing_name(self, client):
        """Test adding student without name returns error"""
        data = {'email': 'test@example.com'}
        response = client.post('/add-student', data=data)
        assert response.status_code == 400  # Bad request
    
    def test_edit_student_get(self, client, sample_student):
        """Test GET request to edit student"""
        # First add a student
        client.post('/add-student', data=sample_student, follow_redirects=True)
        
        # Then try to edit it
        response = client.get('/edit-student/1')
        assert response.status_code == 200
    
    def test_edit_student_not_found(self, client):
        """Test editing non-existent student returns 404"""
        response = client.get('/edit-student/999')
        assert response.status_code == 404
    
    def test_delete_student(self, client, sample_student):
        """Test deleting a student"""
        # Add student
        client.post('/add-student', data=sample_student, follow_redirects=True)
        
        # Delete student
        response = client.post('/delete-student/1', follow_redirects=True)
        assert response.status_code == 200


# ==================== API ENDPOINT TESTS ====================

class TestAPIEndpoints:
    """Test REST API endpoints"""
    
    def test_api_get_all_students(self, client, sample_student):
        """Test API endpoint to get all students"""
        # Add student
        client.post('/add-student', data=sample_student, follow_redirects=True)
        
        # Get via API
        response = client.get('/api/students')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert len(data['data']) == 1
        assert data['count'] == 1
    
    def test_api_get_single_student(self, client, sample_student):
        """Test API endpoint to get single student"""
        # Add student
        client.post('/add-student', data=sample_student, follow_redirects=True)
        
        # Get via API
        response = client.get('/api/students/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['name'] == sample_student['name']
    
    def test_api_get_student_not_found(self, client):
        """Test API endpoint for non-existent student"""
        response = client.get('/api/students/999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] is False


# ==================== ERROR HANDLING TESTS ====================

class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_404_error(self, client):
        """Test 404 error page"""
        response = client.get('/nonexistent-page')
        assert response.status_code == 404
    
    def test_page_with_special_characters(self, client, sample_student):
        """Test handling special characters in form data"""
        data = sample_student.copy()
        data['name'] = "John O'Donnell"
        data['major'] = 'Computer Science & Engineering'
        
        response = client.post('/add-student', data=data, follow_redirects=True)
        assert response.status_code == 200


# ==================== INTEGRATION TESTS ====================

class TestIntegration:
    """Integration tests - test multiple operations together"""
    
    def test_full_student_lifecycle(self, client, sample_student):
        """Test complete student lifecycle: add, view, edit, delete"""
        # 1. Add student
        response = client.post('/add-student', data=sample_student, follow_redirects=True)
        assert response.status_code == 200
        
        # 2. View students
        response = client.get('/students')
        assert response.status_code == 200
        assert sample_student['name'].encode() in response.data
        
        # 3. Edit student
        updated_data = sample_student.copy()
        updated_data['grade'] = 'Senior'
        response = client.post('/edit-student/1', data=updated_data, follow_redirects=True)
        assert response.status_code == 200
        
        # 4. Delete student
        response = client.post('/delete-student/1', follow_redirects=True)
        assert response.status_code == 200
        
        # 5. Verify student is deleted
        response = client.get('/students')
        assert sample_student['name'].encode() not in response.data
    
    def test_multiple_students_workflow(self, client):
        """Test workflow with multiple students"""
        students = [
            {'name': 'Alice', 'email': 'alice@example.com'},
            {'name': 'Bob', 'email': 'bob@example.com'},
            {'name': 'Charlie', 'email': 'charlie@example.com'}
        ]
        
        # Add multiple students
        for student in students:
            client.post('/add-student', data=student, follow_redirects=True)
        
        # Verify all students exist
        response = client.get('/api/students')
        data = json.loads(response.data)
        assert data['count'] == 3


# ==================== PERFORMANCE TESTS ====================

class TestPerformance:
    """Test performance and scalability"""
    
    def test_bulk_student_operations(self, student_mgr):
        """Test adding many students"""
        # Add 100 students
        for i in range(100):
            student_mgr.add_student({
                'name': f'Student {i}',
                'email': f'student{i}@example.com'
            })
        
        # Verify all were added
        students = student_mgr.get_all_students()
        assert len(students) == 100


# ==================== TEST EXECUTION ====================

if __name__ == '__main__':
    """
    Run tests with pytest:
    pytest tests/test_app.py
    
    Run with coverage:
    pytest --cov=. tests/test_app.py
    
    Run specific test:
    pytest tests/test_app.py::TestStudentManager::test_add_student
    """
    pytest.main([__file__, '-v'])
