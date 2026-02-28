from flask import Blueprint, request, jsonify
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from models.user import User, db
from decorators import token_required

location_bp = Blueprint('location', __name__, url_prefix='/api/location')

# Initialize Nominatim with a unique user agent
geolocator = Nominatim(user_agent="pivot_productivity_app_v1")


@location_bp.route('/verify', methods=['POST'])
@token_required
def verify_location(current_user):
    """
    Verify user location against a target address
    
    Request body:
    {
        "lat": 40.7128,
        "lng": -74.0060,
        "target_address": "123 Main St, New York, NY"
    }
    
    Returns productivity status:
    - GREEN: < 200m (at location)
    - YELLOW: 200-1000m (nearby)
    - RED: > 1000m (far away)
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'lat' not in data or 'lng' not in data or 'target_address' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields: lat, lng, target_address'
            }), 400
        
        user_gps = (data['lat'], data['lng'])
        target_address = data['target_address'].strip()
        
        # 1. Convert Address to Coordinates (Geocoding)
        location = geolocator.geocode(target_address, timeout=10)
        
        if not location:
            return jsonify({
                'status': 'error',
                'message': 'Address not found'
            }), 404
        
        target_gps = (location.latitude, location.longitude)
        
        # 2. Calculate Distance using geodesic (accurate for Earth's curvature)
        distance_meters = geodesic(user_gps, target_gps).meters
        
        # 3. Productivity Logic - determine status based on distance
        status = "RED"
        if distance_meters < 200:
            status = "GREEN"  # Within 200 meters of task
        elif distance_meters < 1000:
            status = "YELLOW"  # Nearby, but not at location
        
        # Update user's last verified location
        current_user.last_verified_location = location.address
        current_user.last_verified_lat = location.latitude
        current_user.last_verified_lng = location.longitude
        current_user.last_verification_time = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'user_id': current_user.id,
            'productivity_status': status,
            'distance_meters': round(distance_meters, 2),
            'verified_address': location.address,
            'verified_coordinates': {
                'latitude': location.latitude,
                'longitude': location.longitude
            },
            'proximity_details': {
                'at_location': status == 'GREEN',
                'nearby': status == 'YELLOW',
                'far_away': status == 'RED'
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Location verification failed: {str(e)}'
        }), 500


@location_bp.route('/history', methods=['GET'])
@token_required
def get_location_history(current_user):
    """Get user's last verified location"""
    return jsonify({
        'status': 'success',
        'user': {
            'id': current_user.id,
            'username': current_user.username,
            'last_verified_location': current_user.last_verified_location,
            'last_verified_coordinates': {
                'latitude': current_user.last_verified_lat,
                'longitude': current_user.last_verified_lng
            } if current_user.last_verified_lat else None,
            'last_verification_time': current_user.last_verification_time.isoformat() if current_user.last_verification_time else None
        }
    }), 200
