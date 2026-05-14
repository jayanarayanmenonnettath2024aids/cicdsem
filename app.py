"""
Cloud-Based Student Management System - Main Flask Application
This is a beginner-friendly DevOps CI/CD demo project using Python and AWS.

Author: DevOps Learning Project
Purpose: Demonstrate CI/CD pipeline with AWS CodeBuild, CodePipeline, and GitHub Actions
"""

# Import required libraries
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import logging
import os
import sys

# Import our custom student management module
from routes.student_manager import StudentManager

# ==================== FLASK APP INITIALIZATION ====================
# Create Flask application instance
# This is the main entry point for the web application
app = Flask(__name__)

# Set application configuration
app.config['JSON_SORT_KEYS'] = False  # Keep JSON keys in order

# ==================== LOGGING SETUP ====================
# Configure logging for production-ready monitoring
# This is important for debugging and understanding application behavior
logging.basicConfig(
    level=logging.INFO,  # Set logging level to INFO
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    handlers=[
        logging.FileHandler('app.log'),  # Write logs to file
        logging.StreamHandler()  # Also print to console
    ]
)
logger = logging.getLogger(__name__)

# ==================== INITIALIZE STUDENT MANAGER ====================
# Create an instance of StudentManager to handle all student operations
# The StudentManager class handles CRUD operations (Create, Read, Update, Delete)
student_manager = StudentManager()

# Log application startup
logger.info("Student Management System application started")


# ==================== HEALTH CHECK ENDPOINT ====================
@app.route('/health', methods=['GET'])
def health_check():
    """
    Health Check Endpoint
    
    This endpoint is used by:
    - Load balancers to verify the app is running
    - Docker health checks
    - Kubernetes liveness probes
    - AWS ELB/ALB
    
    Returns:
        JSON response indicating application status
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Student Management System'
    }), 200


# ==================== DASHBOARD ROUTE ====================
@app.route('/', methods=['GET'])
@app.route('/dashboard', methods=['GET'])
def dashboard():
    """
    Dashboard Home Page
    
    Displays:
    - Welcome message
    - Quick stats about students
    - Navigation to other pages
    
    Returns:
        Rendered dashboard.html template
    """
    try:
        # Get total number of students
        students = student_manager.get_all_students()
        total_students = len(students)
        
        logger.info(f"Dashboard accessed - Total students: {total_students}")
        
        # Pass data to template
        return render_template('dashboard.html', total_students=total_students)
    
    except Exception as e:
        # Log any errors that occur
        logger.error(f"Error loading dashboard: {str(e)}")
        return render_template('error.html', error=str(e)), 500


# ==================== STUDENTS LIST ROUTE ====================
@app.route('/students', methods=['GET'])
def view_students():
    """
    View All Students Page
    
    Displays:
    - Complete list of all registered students
    - Student details (ID, Name, Email, Phone, Grade)
    - Edit and Delete buttons for each student
    
    Returns:
        Rendered students.html template with student list
    """
    try:
        # Retrieve all students from the database
        students = student_manager.get_all_students()
        
        logger.info(f"Students list accessed - Total: {len(students)}")
        
        return render_template('students.html', students=students)
    
    except Exception as e:
        logger.error(f"Error loading students list: {str(e)}")
        return render_template('error.html', error=str(e)), 500


# ==================== ADD STUDENT ROUTE ====================
@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    """
    Add Student Page and Processing
    
    GET:
        - Displays the form to add a new student
    
    POST:
        - Processes form submission
        - Validates input data
        - Saves new student to database
        - Redirects to students list
    
    Returns:
        GET: Rendered add_student.html form
        POST: Redirect to students list or error page
    """
    if request.method == 'POST':
        try:
            # Extract form data from POST request
            student_data = {
                'name': request.form.get('name', '').strip(),
                'email': request.form.get('email', '').strip(),
                'phone': request.form.get('phone', '').strip(),
                'grade': request.form.get('grade', '').strip(),
                'major': request.form.get('major', '').strip()
            }
            
            # Validate that required fields are not empty
            if not student_data['name'] or not student_data['email']:
                raise ValueError("Name and Email are required fields")
            
            # Add student using StudentManager
            result = student_manager.add_student(student_data)
            
            if result:
                logger.info(f"Student added successfully: {student_data['name']}")
                # Redirect to students list after successful addition
                return redirect(url_for('view_students'))
            else:
                raise ValueError("Failed to add student")
        
        except Exception as e:
            logger.error(f"Error adding student: {str(e)}")
            return render_template('error.html', error=str(e)), 400
    
    # For GET request, show the add student form
    return render_template('add_student.html')


# ==================== EDIT STUDENT ROUTE ====================
@app.route('/edit-student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    """
    Edit Student Page and Processing
    
    GET:
        - Retrieves student data
        - Displays form with existing data pre-filled
    
    POST:
        - Processes form submission
        - Updates student data
        - Redirects to students list
    
    Args:
        student_id: The unique ID of the student to edit
    
    Returns:
        GET: Rendered edit_student.html form with student data
        POST: Redirect to students list or error page
    """
    if request.method == 'POST':
        try:
            # Extract updated student data from form
            updated_data = {
                'name': request.form.get('name', '').strip(),
                'email': request.form.get('email', '').strip(),
                'phone': request.form.get('phone', '').strip(),
                'grade': request.form.get('grade', '').strip(),
                'major': request.form.get('major', '').strip()
            }
            
            # Validate required fields
            if not updated_data['name'] or not updated_data['email']:
                raise ValueError("Name and Email are required fields")
            
            # Update student using StudentManager
            result = student_manager.update_student(student_id, updated_data)
            
            if result:
                logger.info(f"Student updated successfully: ID {student_id}")
                return redirect(url_for('view_students'))
            else:
                raise ValueError("Failed to update student")
        
        except Exception as e:
            logger.error(f"Error updating student: {str(e)}")
            return render_template('error.html', error=str(e)), 400
    
    # For GET request, retrieve student data and show edit form
    try:
        student = student_manager.get_student_by_id(student_id)
        
        if not student:
            raise ValueError(f"Student with ID {student_id} not found")
        
        return render_template('edit_student.html', student=student)
    
    except Exception as e:
        logger.error(f"Error loading student for editing: {str(e)}")
        return render_template('error.html', error=str(e)), 404


# ==================== DELETE STUDENT ROUTE ====================
@app.route('/delete-student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    """
    Delete Student Processing
    
    Deletes a student record from the database.
    Uses POST method for safety (prevents accidental deletion via URL)
    
    Args:
        student_id: The unique ID of the student to delete
    
    Returns:
        Redirect to students list or error page
    """
    try:
        # Delete student using StudentManager
        result = student_manager.delete_student(student_id)
        
        if result:
            logger.info(f"Student deleted successfully: ID {student_id}")
            return redirect(url_for('view_students'))
        else:
            raise ValueError("Failed to delete student")
    
    except Exception as e:
        logger.error(f"Error deleting student: {str(e)}")
        return render_template('error.html', error=str(e)), 400


# ==================== API ENDPOINT - GET ALL STUDENTS ====================
@app.route('/api/students', methods=['GET'])
def api_get_students():
    """
    REST API Endpoint - Get All Students
    
    This endpoint is useful for:
    - Frontend JavaScript making AJAX requests
    - Mobile applications
    - Third-party integrations
    
    Returns:
        JSON array of all students
    """
    try:
        students = student_manager.get_all_students()
        logger.info(f"API: Retrieved {len(students)} students")
        
        return jsonify({
            'success': True,
            'data': students,
            'count': len(students)
        }), 200
    
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== API ENDPOINT - GET SINGLE STUDENT ====================
@app.route('/api/students/<int:student_id>', methods=['GET'])
def api_get_student(student_id):
    """
    REST API Endpoint - Get Single Student
    
    Args:
        student_id: The unique ID of the student
    
    Returns:
        JSON object containing student details
    """
    try:
        student = student_manager.get_student_by_id(student_id)
        
        if student:
            return jsonify({
                'success': True,
                'data': student
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Student not found'
            }), 404
    
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors - Page Not Found"""
    logger.warning("404 error - Page not found")
    return render_template('error.html', error="Page not found"), 404


@app.errorhandler(500)
def internal_server_error(error):
    """Handle 500 errors - Internal Server Error"""
    logger.error(f"500 error - Internal server error: {str(error)}")
    return render_template('error.html', error="Internal server error"), 500


# ==================== APPLICATION STARTUP ====================
if __name__ == '__main__':
    """
    Main Application Entry Point
    
    This code runs when the script is executed directly
    (not when imported as a module)
    
    Development: Set debug=True for auto-reload and debugger
    Production: Set debug=False and use WSGI server (Gunicorn, uWSGI)
    """
    
    # Determine if running in debug mode based on environment variable
    # DEBUG should be False in production
    debug_mode = os.getenv('FLASK_ENV', 'development') == 'development'
    
    # Get port from environment variable or use default 5000
    port = int(os.getenv('PORT', 5000))
    
    logger.info(f"Starting Flask app on port {port} (Debug: {debug_mode})")
    
    # Start the Flask development server
    # Host 0.0.0.0 makes the app accessible from any network interface
    app.run(
        host='0.0.0.0',  # Listen on all network interfaces
        port=port,  # Use configured port
        debug=debug_mode  # Enable/disable debug mode
    )
