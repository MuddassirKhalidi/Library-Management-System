"""
FR2: Member Registration and Management

Test Cases:
- TC2.1: Register New Member
- TC2.2: Update Member Information
- TC2.3: Deactivate Membership
"""

import pytest
from unittest.mock import MagicMock
from library_system.models.member import Member
from library_system.utils.enums import MemberStatus


class TestFR2MemberManagement:
    """Test cases for FR2: Member Registration and Management."""
    
    def test_tc2_1_register_new_member(self, member_service, mock_db_client, sample_member):
        """
        TC2.1: Register New Member
        
        Test Item: MemberService.register_member()
        Input Specification:
            Name: 'Ali'
            Email: 'ali@test.com'
            Status: Active
        Expected Output:
            New member created; unique ID assigned
        Environmental / Special Requirements: Database connected
        """
        # Setup: Mock database response
        mock_insert_result = MagicMock()
        mock_insert_result.data = [{
            'member_id': 202,
            'name': 'Ali',
            'email': 'ali@test.com',
            'phone': '1234567890',
            'status': 'active',
            'join_date': '2024-01-01'
        }]
        
        mock_table = MagicMock()
        mock_table.insert.return_value.execute.return_value = mock_insert_result
        mock_db_client.table.return_value = mock_table
        
        # Execute: Register new member
        created_member = member_service.register_member(sample_member)
        
        # Verify: Member successfully created
        assert created_member is not None
        assert created_member.member_id == 202
        assert created_member.name == 'Ali'
        assert created_member.email == 'ali@test.com'
        assert created_member.status == MemberStatus.ACTIVE
        
        # Verify: Database insert was called
        mock_table.insert.assert_called_once()
        
    def test_tc2_2_update_member_information(self, member_service, mock_db_client, sample_member):
        """
        TC2.2: Update Member Information
        
        Test Item: MemberService.updateMember()
        Input Specification:
            Member ID=202; new phone number
        Expected Output:
            Member information updated
        Environmental / Special Requirements: None
        """
        # Setup: Mock update response
        updated_member_data = {
            'member_id': 202,
            'name': 'Ali',
            'email': 'ali@test.com',
            'phone': '9876543210',  # Updated phone number
            'status': 'active',
            'join_date': '2024-01-01'
        }
        
        mock_update_result = MagicMock()
        mock_update_result.data = [updated_member_data]
        
        mock_table = MagicMock()
        mock_table.update.return_value.eq.return_value.execute.return_value = mock_update_result
        mock_db_client.table.return_value = mock_table
        
        # Execute: Update member
        updated_member = Member(
            member_id=202,
            name='Ali',
            email='ali@test.com',
            phone='9876543210',  # New phone number
            status=MemberStatus.ACTIVE,
            join_date=sample_member.join_date
        )
        
        result = member_service.update_member(202, updated_member)
        
        # Verify: Member information successfully updated
        assert result is not None
        assert result.member_id == 202
        assert result.phone == '9876543210'
        
        # Verify: Update was called with correct parameters
        mock_table.update.assert_called_once()
        mock_table.update.return_value.eq.assert_called_once_with('member_id', 202)
        
    def test_tc2_3_deactivate_membership(self, member_service, mock_db_client):
        """
        TC2.3: Deactivate Membership
        
        Test Item: MemberService.deactivateMember()
        Input Specification: Member ID=202
        Expected Output:
            Member status changed to 'Inactive'
        Environmental / Special Requirements: None
        """
        # Setup: Mock deactivate response
        deactivated_member_data = {
            'member_id': 202,
            'name': 'Ali',
            'email': 'ali@test.com',
            'phone': '1234567890',
            'status': 'inactive',  # Status changed to inactive
            'join_date': '2024-01-01'
        }
        
        mock_update_result = MagicMock()
        mock_update_result.data = [deactivated_member_data]
        
        mock_table = MagicMock()
        mock_table.update.return_value.eq.return_value.execute.return_value = mock_update_result
        mock_db_client.table.return_value = mock_table
        
        # Execute: Deactivate member
        result = member_service.deactivate_member(202)
        
        # Verify: Member successfully deactivated
        assert result is True
        
        # Verify: Update was called with inactive status
        mock_table.update.assert_called_once()
        update_call_args = mock_table.update.call_args[0][0]
        assert update_call_args['status'] == MemberStatus.INACTIVE.value
        mock_table.update.return_value.eq.assert_called_once_with('member_id', 202)

