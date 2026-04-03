import pytest
from root.models import Booking

class TestBookingModel:

    def test_create_booking(self, db_session):
        """Test booking is created correctly"""
        booking = Booking(
            total_to_pay=500.0,
            rest_to_pay=500.0,
            status='pending'
        )
        db_session.session.add(booking)
        db_session.session.commit()

        assert booking.id is not None
        assert booking.total_to_pay == 500.0
        assert booking.status == 'pending'

    def test_default_values(self, db_session):
        """Test model default values"""
        booking = Booking(total_to_pay=300.0)
        db_session.session.add(booking)
        db_session.session.commit()

        assert booking.status == 'cancelled'
        assert booking.refund == 0

    def test_invalid_status(self, db_session):
        """Test that invalid status raises error"""
        booking = Booking(total_to_pay=300.0)
        with pytest.raises(ValueError):
            booking.status = 'invalid_status'

    def test_update_booking(self, sample_booking, db_session):
        """Test updating a booking"""
        sample_booking.rest_to_pay = 0
        db_session.session.commit()

        updated = Booking.query.get(sample_booking.id)
        assert updated.rest_to_pay == 0
        assert updated.status == 'paid'   # from your event listener

    def test_delete_booking(self, sample_booking, db_session):
        """Test deleting a booking"""
        booking_id = sample_booking.id
        db_session.session.delete(sample_booking)
        db_session.session.commit()

        assert Booking.query.get(booking_id) is None