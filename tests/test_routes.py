from root.financier import financial_bp
from flask import url_for
class TestBookingRoutes:

    def test_get_bookings_page(self, client):
        """Test that bookings page loads correctly"""
        response = client.get(url_for("financial_bp.bookings"))
        assert response.status_code == 200

    def test_get_booking_modal(self, client, sample_booking):
        """Test modal endpoint returns HTML"""
        response = client.get(f'/booking/{sample_booking.id}/modal')
        assert response.status_code == 200
        data = response.get_json()
        assert 'html' in data
        assert str(sample_booking.id) in data['html']

    def test_create_booking_post(self, client):
        """Test POST to create a booking"""
        response = client.post('/booking/add', data={
            'total_to_pay': 800.0,
            'status': 'pending'
        })
        assert response.status_code in [200, 302]  # 302 = redirect after success

    def test_booking_not_found(self, client):
        """Test 404 for non-existent booking"""
        response = client.get('/booking/99999/modal')
        assert response.status_code == 404

    def test_delete_booking(self, client, sample_booking):
        """Test deleting a booking via route"""
        response = client.post(f'/booking/{sample_booking.id}/delete')
        assert response.status_code in [200, 302]

    def test_json_response(self, client, sample_booking):
        """Test that endpoint returns valid JSON"""
        response = client.get(f'/booking/{sample_booking.id}/modal')
        assert response.content_type == 'application/json'
