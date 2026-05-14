"""
Student Manager Module
Handles all student-related database operations (CRUD operations)
"""

import json
import os
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Get absolute path to project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database file path
DATABASE_FILE = os.path.join(BASE_DIR, "..", "students_db.json")


class StudentManager:
    """
    Student Manager Class
    Handles CRUD operations for students
    """

    def __init__(self):
        """
        Initialize database
        """
        self.db_file = DATABASE_FILE
        self._initialize_database()

    def _initialize_database(self):
        """
        Create database file if it doesn't exist
        """
        try:
            if not os.path.exists(self.db_file):

                initial_data = {
                    "students": [],
                    "next_id": 1,
                    "created_at": datetime.now().isoformat()
                }

                with open(self.db_file, "w") as f:
                    json.dump(initial_data, f, indent=2)

                logger.info(f"Database initialized: {self.db_file}")

        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            raise

    def _load_database(self):
        """
        Load database from JSON file
        """
        try:
            with open(self.db_file, "r") as f:
                return json.load(f)

        except Exception as e:
            logger.error(f"Error loading database: {str(e)}")
            raise

    def _save_database(self, data):
        """
        Save database to JSON file
        """
        try:
            with open(self.db_file, "w") as f:
                json.dump(data, f, indent=2)

            logger.info("Database saved successfully")

        except Exception as e:
            logger.error(f"Error saving database: {str(e)}")
            raise

    def add_student(self, student_data):
        """
        Add a new student
        """
        try:
            if not student_data.get("name") or not student_data.get("email"):
                raise ValueError("Name and Email are required")

            db = self._load_database()

            new_student = {
                "id": db["next_id"],
                "name": student_data["name"],
                "email": student_data["email"],
                "phone": student_data.get("phone", ""),
                "grade": student_data.get("grade", ""),
                "major": student_data.get("major", ""),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }

            db["students"].append(new_student)
            db["next_id"] += 1

            self._save_database(db)

            logger.info(f"Student added: {new_student['name']}")

            return new_student

        except Exception as e:
            logger.error(f"Error adding student: {str(e)}")
            raise

    def get_all_students(self):
        """
        Get all students
        """
        try:
            db = self._load_database()
            return db.get("students", [])

        except Exception as e:
            logger.error(f"Error getting students: {str(e)}")
            raise

    def get_student_by_id(self, student_id):
        """
        Get student by ID
        """
        try:
            db = self._load_database()

            for student in db.get("students", []):
                if student["id"] == int(student_id):
                    return student

            return None

        except Exception as e:
            logger.error(f"Error getting student: {str(e)}")
            raise

    def update_student(self, student_id, updated_data):
        """
        Update student details
        """
        try:
            db = self._load_database()

            for student in db.get("students", []):

                if student["id"] == int(student_id):

                    student["name"] = updated_data.get("name", student["name"])
                    student["email"] = updated_data.get("email", student["email"])
                    student["phone"] = updated_data.get("phone", student["phone"])
                    student["grade"] = updated_data.get("grade", student["grade"])
                    student["major"] = updated_data.get("major", student["major"])
                    student["updated_at"] = datetime.now().isoformat()

                    self._save_database(db)

                    logger.info(f"Student updated: ID {student_id}")

                    return student

            return None

        except Exception as e:
            logger.error(f"Error updating student: {str(e)}")
            raise

    def delete_student(self, student_id):
        """
        Delete student
        """
        try:
            db = self._load_database()

            for i, student in enumerate(db.get("students", [])):

                if student["id"] == int(student_id):

                    db["students"].pop(i)

                    self._save_database(db)

                    logger.info(f"Student deleted: ID {student_id}")

                    return True

            return False

        except Exception as e:
            logger.error(f"Error deleting student: {str(e)}")
            raise

    def get_student_count(self):
        """
        Get total student count
        """
        try:
            db = self._load_database()
            return len(db.get("students", []))

        except Exception as e:
            logger.error(f"Error getting count: {str(e)}")
            return 0

    def search_students(self, query):
        """
        Search students
        """
        try:
            db = self._load_database()

            query_lower = query.lower()

            results = [
                student for student in db.get("students", [])
                if query_lower in student["name"].lower()
                or query_lower in student["email"].lower()
            ]

            return results

        except Exception as e:
            logger.error(f"Error searching students: {str(e)}")
            return []

    def clear_all_students(self):
        """
        Clear database
        """
        try:
            db = self._load_database()

            db["students"] = []
            db["next_id"] = 1

            self._save_database(db)

            logger.warning("Database cleared")

            return True

        except Exception as e:
            logger.error(f"Error clearing database: {str(e)}")
            raise
