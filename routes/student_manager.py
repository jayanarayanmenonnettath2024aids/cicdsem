"""
Student Manager Module
Handles all student-related database operations (CRUD operations)

This module provides an abstraction layer for student data management.
It currently uses JSON for storage but can easily be modified to use:
- SQLite
- PostgreSQL
- DynamoDB
- Other databases

Purpose: Demonstrate how to structure code in a production-ready way
"""

import json
import os
from datetime import datetime
from pathlib import Path
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Database file path - stores all student data in JSON format
# In production, this would be a database like PostgreSQL
DATABASE_FILE = 'students_db.json'


class StudentManager:
    """
    Student Manager Class
    
    Handles all database operations for student management:
    - Add students
    - Update students
    - Delete students
    - Retrieve students
    
    This class demonstrates:
    - Object-oriented programming (OOP)
    - Data persistence
    - Error handling
    - Logging
    """
    
    def __init__(self):
        """
        Initialize StudentManager
        
        Performs:
        - Checks if database file exists
        - Creates it if it doesn't exist
        - Loads existing data
        """
        self.db_file = DATABASE_FILE
        self._initialize_database()
    
    def _initialize_database(self):
        """
        Initialize the database file
        
        Creates an empty database if it doesn't exist
        This ensures the application can start even if database is missing
        """
        try:
            # Check if database file exists
            if not os.path.exists(self.db_file):
                # Create new database with empty student list
                initial_data = {
                    'students': [],
                    'next_id': 1,
                    'created_at': datetime.now().isoformat()
                }
                
                # Write initial data to file
                with open(self.db_file, 'w') as f:
                    json.dump(initial_data, f, indent=2)
                
                logger.info(f"Database initialized: {self.db_file}")
        
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            raise
    
    def _load_database(self):
        """
        Load database from file
        
        Returns:
            Dictionary containing all database data
        
        Raises:
            Exception: If file cannot be read
        """
        try:
            with open(self.db_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading database: {str(e)}")
            raise
    
    def _save_database(self, data):
        """
        Save database to file
        
        Args:
            data: Dictionary to save to database file
        
        Raises:
            Exception: If file cannot be written
        """
        try:
            with open(self.db_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info("Database saved successfully")
        except Exception as e:
            logger.error(f"Error saving database: {str(e)}")
            raise
    
    def add_student(self, student_data):
        """
        Add a new student to the database
        
        Args:
            student_data: Dictionary containing student information
                - name: Student's full name (required)
                - email: Student's email address (required)
                - phone: Student's phone number
                - grade: Student's current grade/year
                - major: Student's major/field of study
        
        Returns:
            Dictionary containing the added student with assigned ID
        
        Raises:
            ValueError: If required fields are missing
            Exception: If database operation fails
        """
        try:
            # Validate required fields
            if not student_data.get('name') or not student_data.get('email'):
                raise ValueError("Name and Email are required fields")
            
            # Load current database
            db = self._load_database()
            
            # Create new student object with auto-incremented ID
            new_student = {
                'id': db['next_id'],
                'name': student_data['name'],
                'email': student_data['email'],
                'phone': student_data.get('phone', ''),
                'grade': student_data.get('grade', ''),
                'major': student_data.get('major', ''),
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            # Add student to database
            db['students'].append(new_student)
            
            # Increment ID for next student
            db['next_id'] += 1
            
            # Save updated database
            self._save_database(db)
            
            logger.info(f"Student added successfully: {new_student['name']} (ID: {new_student['id']})")
            
            return new_student
        
        except Exception as e:
            logger.error(f"Error adding student: {str(e)}")
            raise
    
    def get_all_students(self):
        """
        Retrieve all students from database
        
        Returns:
            List of all student dictionaries
        
        Raises:
            Exception: If database operation fails
        """
        try:
            db = self._load_database()
            students = db.get('students', [])
            logger.info(f"Retrieved {len(students)} students from database")
            return students
        except Exception as e:
            logger.error(f"Error retrieving students: {str(e)}")
            raise
    
    def get_student_by_id(self, student_id):
        """
        Retrieve a single student by ID
        
        Args:
            student_id: The unique ID of the student to retrieve
        
        Returns:
            Student dictionary if found, None otherwise
        
        Raises:
            Exception: If database operation fails
        """
        try:
            db = self._load_database()
            
            # Search for student with matching ID
            for student in db.get('students', []):
                if student['id'] == int(student_id):
                    logger.info(f"Student found: ID {student_id}")
                    return student
            
            # Student not found
            logger.warning(f"Student not found: ID {student_id}")
            return None
        
        except Exception as e:
            logger.error(f"Error retrieving student: {str(e)}")
            raise
    
    def update_student(self, student_id, updated_data):
        """
        Update an existing student's information
        
        Args:
            student_id: The unique ID of the student to update
            updated_data: Dictionary containing updated student information
        
        Returns:
            Updated student dictionary if successful, None otherwise
        
        Raises:
            Exception: If database operation fails
        """
        try:
            db = self._load_database()
            
            # Find and update the student
            for i, student in enumerate(db.get('students', [])):
                if student['id'] == int(student_id):
                    # Update student fields
                    student['name'] = updated_data.get('name', student['name'])
                    student['email'] = updated_data.get('email', student['email'])
                    student['phone'] = updated_data.get('phone', student['phone'])
                    student['grade'] = updated_data.get('grade', student['grade'])
                    student['major'] = updated_data.get('major', student['major'])
                    student['updated_at'] = datetime.now().isoformat()
                    
                    # Save updated database
                    self._save_database(db)
                    
                    logger.info(f"Student updated successfully: ID {student_id}")
                    
                    return student
            
            # Student not found
            logger.warning(f"Student not found for update: ID {student_id}")
            return None
        
        except Exception as e:
            logger.error(f"Error updating student: {str(e)}")
            raise
    
    def delete_student(self, student_id):
        """
        Delete a student from the database
        
        Args:
            student_id: The unique ID of the student to delete
        
        Returns:
            True if deletion successful, False otherwise
        
        Raises:
            Exception: If database operation fails
        """
        try:
            db = self._load_database()
            
            # Find and remove the student
            for i, student in enumerate(db.get('students', [])):
                if student['id'] == int(student_id):
                    # Remove student from list
                    removed_student = db['students'].pop(i)
                    
                    # Save updated database
                    self._save_database(db)
                    
                    logger.info(f"Student deleted successfully: {removed_student['name']} (ID: {student_id})")
                    
                    return True
            
            # Student not found
            logger.warning(f"Student not found for deletion: ID {student_id}")
            return False
        
        except Exception as e:
            logger.error(f"Error deleting student: {str(e)}")
            raise
    
    def get_student_count(self):
        """
        Get total number of students in database
        
        Returns:
            Integer count of total students
        """
        try:
            db = self._load_database()
            count = len(db.get('students', []))
            return count
        except Exception as e:
            logger.error(f"Error getting student count: {str(e)}")
            return 0
    
    def search_students(self, query):
        """
        Search students by name or email
        
        Args:
            query: Search string (searches in name and email fields)
        
        Returns:
            List of matching students
        """
        try:
            db = self._load_database()
            query_lower = query.lower()
            
            # Search in name and email fields
            results = [
                student for student in db.get('students', [])
                if query_lower in student['name'].lower() or 
                   query_lower in student['email'].lower()
            ]
            
            logger.info(f"Search completed: query='{query}', results={len(results)}")
            return results
        
        except Exception as e:
            logger.error(f"Error searching students: {str(e)}")
            return []
    
    def clear_all_students(self):
        """
        Delete all students from database
        
        WARNING: This operation is irreversible!
        Use only for testing purposes.
        
        Returns:
            True if successful
        """
        try:
            db = self._load_database()
            db['students'] = []
            db['next_id'] = 1
            self._save_database(db)
            logger.warning("All students cleared from database")
            return True
        except Exception as e:
            logger.error(f"Error clearing database: {str(e)}")
            raise
