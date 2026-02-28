# Quick Start Guide

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask & Flask-SQLAlchemy for backend
- JWT for authentication tokens
- geopy for location verification (geocoding & distance calculation)

## 2. Run the Backend Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

You should see output like:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

## 3. Test the API (Optional)

In another terminal, run:
```bash
python test_api.py
```

This will run all tests and show you if everything is working correctly.

## 4. API Endpoints Ready to Use

Your backend now has these endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/auth/signup` | Create new user |
| POST | `/api/auth/login` | Login user |
| GET | `/api/auth/profile` | Get user profile (requires token) |
| POST | `/api/auth/logout` | Logout (requires token) |
| POST | `/api/location/verify` | Verify user location against address |
| GET | `/api/location/history` | Get last verified location |

## 5. Integrate with Flutter

See [FLUTTER_INTEGRATION.md](FLUTTER_INTEGRATION.md) for complete Flutter integration examples.

### Location Verification

For location-based task verification, see [LOCATION_API.md](LOCATION_API.md) for:
- Getting user GPS location
- Verifying against task addresses
- Distance calculation
- Productivity status (GREEN/YELLOW/RED)

### Quick Summary for Flutter:
1. Add `http` package to `pubspec.yaml`
2. Create `AuthService` class to call API endpoints
3. Use `SharedPreferences` to store JWT tokens
4. Include token in `Authorization: Bearer <token>` header for protected routes

## 6. Database

SQLite database automatically created as `users.db` on first run.

To reset database, delete `users.db` and restart the server.

## 7. Security Checklist

Before deploying to production:
- [ ] Change `SECRET_KEY` in `app.py`
- [ ] Switch from SQLite to PostgreSQL/MySQL
- [ ] Use HTTPS instead of HTTP
- [ ] Set up proper CORS for your Flutter app domain
- [ ] Use environment variables for sensitive data (see `.env.example`)
- [ ] Add rate limiting to auth endpoints
- [ ] Enable HTTPS in Flutter app

## 8. Common Issues

**"Address already in use"**: Change port in app.py line `app.run(debug=True, host='0.0.0.0', port=5000)`

**CORS errors**: Ensure Flutter app URL is allowed in CORS settings

**Connection timeout from Flutter**: Make sure using correct IP/hostname and port is accessible

**Token invalid errors**: Tokens expire after 30 days, user needs to login again

## 9. Next Steps

- Add email verification
- Implement password reset
- Add user profile update endpoint
- Add refresh tokens
- Set up rate limiting
- Add OAuth/Social login
- Deploy to production server (Heroku, AWS, DigitalOcean, etc.)

## 10. File Structure

```
hackillinois/
├── app.py                    # Main Flask application
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── README.md                 # Full documentation
├── FLUTTER_INTEGRATION.md    # Flutter integration guide
├── QUICK_START.md            # This file
├── test_api.py               # API testing script
└── users.db                  # SQLite database (auto-created)
```

## 11. Useful cURL Commands for Testing

**Signup:**
```bash
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"pass123"}'
```

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"pass123"}'
```

**Get Profile (replace TOKEN):**
```bash
curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer TOKEN"
```

---

**You're all set!** Your authentication backend is ready for integration with Flutter. 🚀
