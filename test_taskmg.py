import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
from datetime import datetime

# Import the functions from your script
import taskmg

class TestTaskMgmt(unittest.TestCase):

    def setUp(self):
        """Set up some initial data for testing."""
        self.sample_tasks = [
            {
                "id": 1,
                "description": "Test task 1",
                "status": "pending",
                "createat": "2023-01-01 12:00:00",
                "updateat": "2023-01-01 12:00:00"
            },
            {
                "id": 2,
                "description": "Test task 2",
                "status": "complete",
                "createat": "2023-01-02 12:00:00",
                "updateat": "2023-01-02 12:00:00"
            }
        ]
        # Mock datetime to return a fixed value
        self.mock_datetime = patch('taskmg.datetime').start()
        self.mock_datetime.now.return_value = datetime(2023, 10, 27, 10, 0, 0)

    def tearDown(self):
        """Stop all patches."""
        patch.stopall()

    @patch('taskmg.read_tasks')
    @patch('taskmg.write_file')
    def test_save_tasks(self, mock_write_file, mock_read_tasks):
        """Test adding a new task."""
        # Arrange: Start with an empty list of tasks
        mock_read_tasks.return_value = []
        
        # Act: Call the function to save a new task
        taskmg.save_tasks("New test task", "new_status")
        
        # Assert: Check that write_file was called exactly once
        mock_write_file.assert_called_once()
        
        # Get the data that write_file was called with
        written_data = mock_write_file.call_args[0][0]
        
        self.assertEqual(len(written_data), 1)
        self.assertEqual(written_data[0]['description'], "New test task")
        self.assertEqual(written_data[0]['status'], "new_status")
        self.assertEqual(written_data[0]['id'], 1) # First task should have ID 1
        self.assertEqual(written_data[0]['createat'], "2023-10-27 10:00:00")

    @patch('taskmg.read_tasks')
    @patch('taskmg.write_file')
    @patch('builtins.print')
    def test_update_task_success(self, mock_print, mock_write_file, mock_read_tasks):
        """Test successfully updating an existing task."""
        # Arrange: read_tasks will return a copy of our sample data
        mock_read_tasks.return_value = [task.copy() for task in self.sample_tasks]
        
        # Act: Update task 1
        taskmg.update_task(1, "Updated description", "in progress")
        
        # Assert: Check that the file was written to
        mock_write_file.assert_called_once()
        written_data = mock_write_file.call_args[0][0]
        
        self.assertEqual(written_data[0]['description'], "Updated description")
        self.assertEqual(written_data[0]['status'], "in progress")
        self.assertEqual(written_data[0]['updateat'], "2023-10-27 10:00:00")
        mock_print.assert_called_with("Task 1 updated successfully.")

    @patch('taskmg.read_tasks')
    @patch('taskmg.write_file')
    @patch('builtins.print')
    def test_update_task_not_found(self, mock_print, mock_write_file, mock_read_tasks):
        """Test updating a task that does not exist."""
        mock_read_tasks.return_value = self.sample_tasks
        
        taskmg.update_task(99, "Non-existent", "non-existent")
        
        mock_write_file.assert_not_called() # Should not write if task not found
        mock_print.assert_called_with("Error: Task with ID 99 not found.")

    @patch('taskmg.read_tasks')
    @patch('taskmg.write_file')
    @patch('builtins.print')
    def test_delete_task_success(self, mock_print, mock_write_file, mock_read_tasks):
        """Test successfully deleting a task."""
        mock_read_tasks.return_value = [task.copy() for task in self.sample_tasks]
        
        taskmg.delete_task(1)
        
        mock_write_file.assert_called_once()
        written_data = mock_write_file.call_args[0][0]
        
        self.assertEqual(len(written_data), 1)
        self.assertEqual(written_data[0]['id'], 2) # Only task with ID 2 should remain
        mock_print.assert_called_with("Task 1 has been deleted successfully.")

    @patch('taskmg.read_tasks')
    @patch('taskmg.write_file')
    @patch('builtins.print')
    def test_delete_task_not_found(self, mock_print, mock_write_file, mock_read_tasks):
        """Test deleting a task that does not exist."""
        mock_read_tasks.return_value = self.sample_tasks
        
        taskmg.delete_task(99)
        
        mock_write_file.assert_not_called()
        mock_print.assert_called_with("Error: Task with ID 99 not found.")
        
    @patch('taskmg.read_tasks')
    @patch('builtins.print')
    def test_list_tasks_all(self, mock_print, mock_read_tasks):
        """Test listing all tasks."""
        mock_read_tasks.return_value = self.sample_tasks
        
        taskmg.list_tasks()
        
        # Check that print was called multiple times (for header, tasks, footer)
        self.assertGreater(mock_print.call_count, len(self.sample_tasks))
        # A simple check to see if one of the task descriptions was printed
        printed_output = " ".join([call[0][0] for call in mock_print.call_args_list])
        self.assertIn("Test task 1", printed_output)
        self.assertIn("Test task 2", printed_output)
        
    @patch('taskmg.read_tasks')
    @patch('builtins.print')
    def test_list_tasks_filtered(self, mock_print, mock_read_tasks):
        """Test listing tasks filtered by status."""
        mock_read_tasks.return_value = self.sample_tasks
        
        taskmg.list_tasks(status="pending")
        
        printed_output = " ".join([call[0][0] for call in mock_print.call_args_list])
        self.assertIn("Test task 1", printed_output)
        self.assertNotIn("Test task 2", printed_output)

    @patch('taskmg.read_tasks')
    @patch('builtins.print')
    def test_list_tasks_empty(self, mock_print, mock_read_tasks):
        """Test listing when no tasks exist."""
        mock_read_tasks.return_value = []
        
        taskmg.list_tasks()
        
        mock_print.assert_called_once_with("Your task list is empty! Go add something to do.")

if __name__ == '__main__':
    unittest.main()
