"""
FR8: Authentication and Role-Based Access

Test Cases:
- TC8.1: Librarian Login Success
- TC8.2: Member Access Restricted
"""

import pytest
from unittest.mock import MagicMock
from library_system.models.user import User
from library_system.utils.enums import RoleName


class TestFR8Authentication:
    """Test cases for FR8: Authentication and Role-Based Access."""
    
    def test_tc8_1_librarian_login_success(self, auth_service, mock_db_client):
        """
        TC8.1: Librarian Login Success
        
        Test Item: AuthService.login()
        Input Specification:
            Username: 'librarian'
            Password: '12345'
        Expected Output:
            Login successful; redirected to dashboard
        Environmental / Special Requirements: None
        """
        # Setup: Mock user lookup and password hash
        # The password '12345' will be hashed using SHA256
        import hashlib
        password_hash = hashlib.sha256('12345'.encode()).hexdigest()
        
        mock_user_result = MagicMock()
        mock_user_result.data = [{
            'user_id': 1,
            'name': 'Librarian',
            'email': 'librarian@library.com',
            'password_hash': password_hash,
            'role': 'librarian'
        }]
        
        mock_table = MagicMock()
        mock_table.select.return_value.eq.return_value.execute.return_value = mock_user_result
        mock_db_client.table.return_value = mock_table
        
        # Execute: Authenticate librarian
        user = auth_service.authenticate(email='librarian@library.com', password='12345')
        
        # Verify: Login successful
        assert user is not None
        assert user.user_id == 1
        assert user.email == 'librarian@library.com'
        assert user.role == RoleName.LIBRARIAN
        
        # Verify: Database query was made
        mock_table.select.assert_called_once()
        
    def test_tc8_2_member_access_restricted(self, auth_service, sample_member_user):
        """
        TC8.2: Member Access Restricted
        
        Test Item: AuthService.accessControl()
        Input Specification:
            Role: 'Member'
            Action: 'Delete Book'
        Expected Output:
            Access denied message displayed
        Environmental / Special Requirements: None
        """
        # Execute: Check if member can manage books (which includes delete)
        can_manage_books = auth_service.can_manage_books(sample_member_user)
        
        # Verify: Access denied for member role
        assert can_manage_books is False
        
        # Execute: Check if member can manage members
        can_manage_members = auth_service.can_manage_members(sample_member_user)
        
        # Verify: Access denied for member role
        assert can_manage_members is False
        
        # Execute: Check role-based access
        has_librarian_role = auth_service.has_role(sample_member_user, [RoleName.LIBRARIAN, RoleName.ADMINISTRATOR])
        
        # Verify: Member does not have librarian or administrator role
        assert has_librarian_role is False
        
        # Additional test: Verify librarian can manage books
        librarian_user = User(
            user_id=1,
            name='Librarian',
            email='librarian@library.com',
            password_hash='hash',
            role=RoleName.LIBRARIAN
        )
        
        can_librarian_manage = auth_service.can_manage_books(librarian_user)
        assert can_librarian_manage is True

