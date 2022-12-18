"""
Test custom Django management commands.
"""
from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# Mock behaviour of check method in defined Command class
@patch("core.management.commands.wait_for_db.Command.check")
class ComandTests(SimpleTestCase):
    "Test commands."

    def test_wait_for_db_ready(self, patched_check):
        "Test waiting for database getting ready"
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    # next patches are added in inside-out order
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        """When db haven't started we receive Psycopg2Error, when
        started yet not ready to take connection - OperationalError
        This is only a way to mock the behaviour of loading db,
        returning succesfull connection after 6th attempt"""
        patched_check.side_effect = [Psycopg2OpError] * 2 \
            + [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
