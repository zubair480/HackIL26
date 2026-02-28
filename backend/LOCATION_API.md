# Location Verification API

## Overview

The location verification feature allows you to:
- Verify user location against a target address
- Calculate distance between user GPS and task location
- Assign productivity status based on proximity
- Track user location history

## How It Works

1. **User GPS**: Location from device GPS
2. **Target Address**: Task location from calendar/app
3. **Geocoding**: Convert address to coordinates using OpenStreetMap/Nominatim
4. **Distance Calculation**: Calculate distance using geodesic (Earth's curvature)
5. **Productivity Status**: Assign status based on distance

## Productivity Status Levels

| Status | Distance | Meaning |
|--------|----------|---------|
| 🟢 GREEN | < 200m | At task location |
| 🟡 YELLOW | 200-1000m | Nearby location |
| 🔴 RED | > 1000m | Far from task |

## API Endpoints

### 1. Verify Location
Verify user's current location against a target address.

```
POST /api/location/verify
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "lat": 40.7580,
  "lng": -73.9855,
  "target_address": "Times Square, New York, NY"
}
```

**Response (200):**
```json
{
  "status": "success",
  "user_id": 1,
  "productivity_status": "GREEN",
  "distance_meters": 45.82,
  "verified_address": "Times Square, New York, New York, United States",
  "verified_coordinates": {
    "latitude": 40.7580,
    "longitude": -73.9855
  },
  "proximity_details": {
    "at_location": true,
    "nearby": false,
    "far_away": false
  }
}
```

**Error Responses:**
- 400: Missing required fields
- 404: Address not found
- 401: Invalid/missing token
- 500: Server error

---

### 2. Get Location History
Retrieve user's last verified location.

```
GET /api/location/history
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "status": "success",
  "user": {
    "id": 1,
    "username": "john_doe",
    "last_verified_location": "Times Square, New York, New York, United States",
    "last_verified_coordinates": {
      "latitude": 40.7580,
      "longitude": -73.9855
    },
    "last_verification_time": "2026-02-28T15:30:00"
  }
}
```

---

## Flutter Integration

### 1. Add Permission to Get User Location

**pubspec.yaml:**
```yaml
dependencies:
  geolocator: ^10.0.0
```

**Android (AndroidManifest.xml):**
```xml
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
```

**iOS (Info.plist):**
```xml
<key>NSLocationWhenInUseUsageDescription</key>
<string>We need your location to verify task attendance</string>
```

### 2. Flutter Location Service

```dart
import 'package:geolocator/geolocator.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class LocationService {
  final String baseUrl = 'http://YOUR_SERVER_IP:5000/api';
  
  Future<Position?> getCurrentLocation() async {
    bool serviceEnabled;
    LocationPermission permission;

    serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      print('Location services are disabled.');
      return null;
    }

    permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        print('Location permissions are denied');
        return null;
      }
    }

    return await Geolocator.getCurrentPosition();
  }

  Future<Map<String, dynamic>> verifyLocation({
    required String token,
    required String targetAddress,
  }) async {
    try {
      Position? position = await getCurrentLocation();
      
      if (position == null) {
        return {
          'status': 'error',
          'message': 'Could not get current location'
        };
      }

      final response = await http.post(
        Uri.parse('$baseUrl/location/verify'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'lat': position.latitude,
          'lng': position.longitude,
          'target_address': targetAddress,
        }),
      ).timeout(const Duration(seconds: 15));

      return jsonDecode(response.body);
    } catch (e) {
      return {
        'status': 'error',
        'message': 'Location verification failed: $e'
      };
    }
  }

  Future<Map<String, dynamic>> getLocationHistory(String token) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/location/history'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
      ).timeout(const Duration(seconds: 10));

      return jsonDecode(response.body);
    } catch (e) {
      return {
        'status': 'error',
        'message': 'Failed to get location history: $e'
      };
    }
  }
}
```

### 3. Flutter UI Widget

```dart
import 'package:flutter/material.dart';
import 'package:your_app/services/location_service.dart';
import 'package:your_app/services/token_service.dart';

class LocationVerificationWidget extends StatefulWidget {
  final String taskAddress;
  final String token;

  const LocationVerificationWidget({
    Key? key,
    required this.taskAddress,
    required this.token,
  }) : super(key: key);

  @override
  State<LocationVerificationWidget> createState() =>
      _LocationVerificationWidgetState();
}

class _LocationVerificationWidgetState
    extends State<LocationVerificationWidget> {
  final _locationService = LocationService();
  bool _isLoading = false;
  Map<String, dynamic>? _result;

  void _verifyLocation() async {
    setState(() => _isLoading = true);

    final result = await _locationService.verifyLocation(
      token: widget.token,
      targetAddress: widget.taskAddress,
    );

    setState(() {
      _result = result;
      _isLoading = false;
    });
  }

  Color _getStatusColor(String status) {
    if (status == 'GREEN') return Colors.green;
    if (status == 'YELLOW') return Colors.orange;
    return Colors.red;
  }

  String _getStatusEmoji(String status) {
    if (status == 'GREEN') return '✓';
    if (status == 'YELLOW') return '⚠';
    return '✗';
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Location Verification',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 16),
            ElevatedButton.icon(
              onPressed: _isLoading ? null : _verifyLocation,
              icon: _isLoading
                  ? const SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : const Icon(Icons.location_on),
              label: const Text('Verify Location'),
            ),
            if (_result != null) ...[
              const SizedBox(height: 16),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: _getStatusColor(_result!['productivity_status'])
                      .withOpacity(0.1),
                  border: Border.all(
                    color: _getStatusColor(_result!['productivity_status']),
                  ),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Text(
                          _getStatusEmoji(_result!['productivity_status']),
                          style: const TextStyle(fontSize: 24),
                        ),
                        const SizedBox(width: 12),
                        Text(
                          _result!['productivity_status'],
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: _getStatusColor(
                                _result!['productivity_status']),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Text(
                      'Distance: ${_result!['distance_meters']} meters',
                      style: const TextStyle(fontSize: 14),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Address: ${_result!['verified_address']}',
                      style: const TextStyle(fontSize: 12),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
              ),
            ] else if (_result != null && _result!['status'] == 'error')
              Text(
                'Error: ${_result!['message']}',
                style: const TextStyle(color: Colors.red),
              )
          ],
        ),
      ),
    );
  }
}
```

## Database Updates

The `users` table now includes location tracking fields:

```sql
last_verified_location VARCHAR(255)     -- Address verified
last_verified_lat FLOAT                 -- Latitude
last_verified_lng FLOAT                 -- Longitude
last_verification_time DATETIME         -- When last verified
```

## Testing with cURL

```bash
# Get token first
TOKEN=$(curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}' | jq -r '.token')

# Verify location
curl -X POST http://localhost:5000/api/location/verify \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "lat": 40.7580,
    "lng": -73.9855,
    "target_address": "Times Square, New York, NY"
  }'

# Get location history
curl -X GET http://localhost:5000/api/location/history \
  -H "Authorization: Bearer $TOKEN"
```

## Notes

- **Nominatim API**: Uses free OpenStreetMap geocoding (rate limited)
- **Timeout**: 10 seconds for address geocoding
- **Accuracy**: Depends on GPS accuracy and address specificity
- **Privacy**: User location is not permanently stored, only last verification
- **Offline**: Location verification requires internet connection

## Future Enhancements

- [ ] Multiple location history entries
- [ ] Geofencing - automatic notifications when entering/leaving area
- [ ] Location-based task scheduling
- [ ] Check-in/Check-out timestamps
- [ ] Location analytics and heatmaps
- [ ] Crowdsourced location data
