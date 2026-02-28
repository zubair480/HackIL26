# Authentication & Location Verification Backend

A Flask-based backend with:
- User signup/login with JWT authentication
- Location verification (GPS to address)
- Distance calculation & productivity status
- Location history tracking

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### 1. Health Check
```
GET /api/health
```
Returns server status.

**Response:**
```json
{
  "status": "success",
  "message": "Backend is running"
}
```

---

### 2. User Signup
```
POST /api/auth/signup
Content-Type: application/json
```

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepass123"
}
```

**Success Response (201):**
```json
{
  "status": "success",
  "message": "User created successfully",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": "2026-02-28T10:30:00"
  }
}
```

**Error Responses:**
- 400: Missing fields or validation errors
- 409: Username or email already exists
- 500: Server error

---

### 3. User Login
```
POST /api/auth/login
Content-Type: application/json
```

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "securepass123"
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": "2026-02-28T10:30:00"
  }
}
```

**Error Responses:**
- 400: Missing fields
- 401: Invalid credentials
- 500: Server error

---

### 4. Get User Profile (Protected)
```
GET /api/auth/profile
Authorization: Bearer <token>
```

**Success Response (200):**
```json
{
  "status": "success",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": "2026-02-28T10:30:00"
  }
}
```

**Error Responses:**
- 401: Missing or invalid token
- 500: Server error

---

### 5. Logout
```
POST /api/auth/logout
Authorization: Bearer <token>
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Logged out successfully"
}
```

---

## Location Verification Endpoints

### 1. Verify Location
```
POST /api/location/verify
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "lat": 40.7128,
  "lng": -74.0060,
  "target_address": "Times Square, New York, NY"
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "user_id": 1,
  "productivity_status": "GREEN",
  "distance_meters": 125.50,
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

**Productivity Status:**
- 🟢 GREEN: Within 200 meters (at location)
- 🟡 YELLOW: 200-1000 meters (nearby)
- 🔴 RED: > 1000 meters (far away)

**Error Responses:**
- 400: Missing fields
- 404: Address not found
- 401: Invalid token
- 500: Server error

---

### 2. Get Location History
```
GET /api/location/history
Authorization: Bearer <token>
```

**Success Response (200):**
```json
{
  "status": "success",
  "user": {
    "id": 1,
    "username": "john_doe",
    "last_verified_location": "Times Square, New York, United States",
    "last_verified_coordinates": {
      "latitude": 40.7580,
      "longitude": -73.9855
    },
    "last_verification_time": "2026-02-28T15:30:00"
  }
}
```

---

## Flutter Integration Guide

See [FLUTTER_INTEGRATION.md](FLUTTER_INTEGRATION.md) for complete Flutter code examples.

### Location Verification Integration

For location-based task verification, see [LOCATION_API.md](LOCATION_API.md) with:
- Get user GPS location
- Verify against task address
- Calculate distance
- Display productivity status

### 1. Add required packages to `pubspec.yaml`:
```yaml
dependencies:
  http: ^1.1.0
  shared_preferences: ^2.2.0
  jwt_decoder: ^2.0.1
```

### 2. Create an API service class:
```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class AuthService {
  final String baseUrl = 'http://localhost:5000/api';
  
  Future<Map<String, dynamic>> signup({
    required String username,
    required String email,
    required String password,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/signup'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'username': username,
        'email': email,
        'password': password,
      }),
    );
    
    return jsonDecode(response.body);
  }
  
  Future<Map<String, dynamic>> login({
    required String username,
    required String password,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'username': username,
        'password': password,
      }),
    );
    
    return jsonDecode(response.body);
  }
  
  Future<Map<String, dynamic>> getProfile(String token) async {
    final response = await http.get(
      Uri.parse('$baseUrl/auth/profile'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
    );
    
    return jsonDecode(response.body);
  }
}
```

### 3. Store token securely using SharedPreferences:
```dart
import 'package:shared_preferences/shared_preferences.dart';

class TokenService {
  static const String _tokenKey = 'auth_token';
  
  Future<void> saveToken(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_tokenKey, token);
  }
  
  Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_tokenKey);
  }
  
  Future<void> clearToken() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_tokenKey);
  }
}
```

## Security Notes

1. **Change the SECRET_KEY** in production to a secure random string
2. **Use HTTPS** in production instead of HTTP
3. **Store tokens securely** in Flutter using secure storage packages
4. **Token Expiry**: Tokens expire after 30 days
5. **Password Hashing**: Passwords are hashed using Werkzeug's security functions
6. **CORS**: Enabled for all origins (configure in production)

## Database

The application uses SQLite (`users.db`) by default. The database file is created automatically on first run.

### Database Schema:
- **users** table:
  - id (Integer, Primary Key)
  - username (String, Unique)
  - email (String, Unique)
  - password (String - hashed)
  - created_at (DateTime)

## Testing with cURL

### Signup:
```bash
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'
```

### Login:
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'
```

### Get Profile (replace TOKEN with actual token):
```bash
curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer TOKEN"
```

## Troubleshooting

- **Port already in use**: Change the port in `app.py` (line with `app.run`)
- **CORS errors**: Ensure Flask-CORS is installed correctly
- **Database issues**: Delete `users.db` to reset the database

## Future Enhancements

- Email verification
- Password reset functionality
- OAuth2/3rd party authentication
- Rate limiting
- Refresh tokens
- User roles/permissions
