"""
Student Manager Module
Handles all student-related database operations (CRUD operations)

This module provides an abstraction layer for student data management.
It uses a JSON file so the project can run locally and inside AWS CodeBuild
without needing an external database service.
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)

# Database file path - stored in the project root so it works on Windows and Linux.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_FILE = Path(os.getenv("STUDENTS_DB_FILE", PROJECT_ROOT / "students_db.json"))


class StudentManager:
    """
    Student Manager Class
    Handles all CRUD operations
    """

    def __init__(self):
        self.db_file = Path(DATABASE_FILE)
        self._initialize_database()

    def _empty_database(self):
        """Create the default database structure."""
        return {
            "students": [],
            "next_id": 1,
            "created_at": datetime.now().isoformat()
        }

    def _ensure_database_exists(self):
        """
        Create the database file if it was deleted.

        AWS CodeBuild and the test suite can start from a clean workspace, so
        every read/write path should recreate the file when needed.
        """
        self.db_file.parent.mkdir(parents=True, exist_ok=True)

        if not self.db_file.exists():
            with open(self.db_file, "w", encoding="utf-8") as f:
                json.dump(self._empty_database(), f, indent=2)

            logger.info(f"Database created at: {self.db_file}")

    def _initialize_database(self):
        """Initialize the database file if it is missing."""
        try:
            self._ensure_database_exists()
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            raise

    # ================================
    # LOAD DATABASE
    # ================================
    def _load_database(self):

        try:
            self._ensure_database_exists()

            with open(self.db_file, "r", encoding="utf-8") as f:
                return json.load(f)

        except Exception as e:
            logger.error(f"Error loading database: {str(e)}")
            raise

    # ================================
    # SAVE DATABASE
    # ================================
    def _save_database(self, data):

        try:
            self._ensure_database_exists()

            with open(self.db_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            logger.info("Database saved successfully")

        except Exception as e:
            logger.error(f"Error saving database: {str(e)}")
            raise

    # ================================
    # ADD STUDENT
    # ================================
    def add_student(self, student_data):

        try:

            if not student_data.get("name"):
                raise ValueError("Student name is required")

            if not student_data.get("email"):
                raise ValueError("Student email is required")

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

    # ================================
    # GET ALL STUDENTS
    # ================================
    def get_all_students(self):

        try:
            db = self._load_database()
            return db.get("students", [])

        except Exception as e:
            logger.error(f"Error getting students: {str(e)}")
            raise

    # ================================
    # GET STUDENT BY ID
    # ================================
    def get_student_by_id(self, student_id):

        try:

            db = self._load_database()

            for student in db.get("students", []):

                if student["id"] == int(student_id):
                    return student

            return None

        except Exception as e:
            logger.error(f"Error getting student: {str(e)}")
            raise

    # ================================
    # UPDATE STUDENT
    # ================================
    def update_student(self, student_id, updated_data):

        try:

            db = self._load_database()

            for student in db.get("students", []):

                if student["id"] == int(student_id):

                    student["name"] = updated_data.get(
                        "name",
                        student["name"]
                    )

                    student["email"] = updated_data.get(
                        "email",
                        student["email"]
                    )

                    student["phone"] = updated_data.get(
                        "phone",
                        student["phone"]
                    )

                    student["grade"] = updated_data.get(
                        "grade",
                        student["grade"]
                    )

                    student["major"] = updated_data.get(
                        "major",
                        student["major"]
                    )

                    student["updated_at"] = datetime.now().isoformat()

                    self._save_database(db)

                    logger.info(f"Student updated: {student_id}")

                    return student

            return None

        except Exception as e:
            logger.error(f"Error updating student: {str(e)}")
            raise

    # ================================
    # DELETE STUDENT
    # ================================
    def delete_student(self, student_id):

        try:

            db = self._load_database()

            for i, student in enumerate(db.get("students", [])):

                if student["id"] == int(student_id):

                    db["students"].pop(i)

                    self._save_database(db)

                    logger.info(f"Student deleted: {student_id}")

                    return True

            return False

        except Exception as e:
            logger.error(f"Error deleting student: {str(e)}")
            raise

    # ================================
    # GET STUDENT COUNT
    # ================================
    def get_student_count(self):

        try:

            db = self._load_database()

            return len(db.get("students", []))

        except Exception as e:
            logger.error(f"Error getting count: {str(e)}")
            return 0

    # ================================
    # SEARCH STUDENTS
    # ================================
    def search_students(self, query):

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

    # ================================
    # CLEAR DATABASE
    # ================================
    def clear_all_students(self):

        try:

            db = self._load_database()

            db["students"] = []
            db["next_id"] = 1

            self._save_database(db)

            logger.warning("All students cleared")

            return True

        except Exception as e:
            logger.error(f"Error clearing database: {str(e)}")
            raise
