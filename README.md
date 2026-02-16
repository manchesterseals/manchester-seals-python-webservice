# Manchester Seals Python Webservice

A Flask-based REST API that connects to MongoDB and provides endpoints to manage roster data.

## 🚀 Quick Start

### Option 1: Using Make (Recommended)
```bash
make setup
make run
```

### Option 2: Using Docker
```bash
docker-compose up -d
```

### Option 3: Manual Setup
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Then visit: `http://localhost:5100/api/health`

---

## 📋 Features

- ✅ Flask REST API framework
- ✅ MongoDB integration with PyMongo
- ✅ Docker & Docker Compose support
- ✅ Environment-based configuration
- ✅ Health check endpoint
- ✅ CRUD operations for roster data
- ✅ Unit tests included
- ✅ Extended version with pagination & search

---

## 📡 API Endpoints

### Basic Version (`app.py`)
- `GET /api/roster` - Get all roster data
- `GET /api/health` - Health check

### Extended Version (`app_extended.py`)
- `GET /api/roster` - Get with pagination & search
- `GET /api/roster/{id}` - Get single entry
- `POST /api/roster` - Create new entry
- `PUT /api/roster/{id}` - Update entry
- `DELETE /api/roster/{id}` - Delete entry
- `GET /api/roster/stats/count` - Total count
- `GET /api/roster/stats/by-department` - Count by department
- `GET /api/info` - API documentation

---

## 🔧 Configuration

Edit `.env` file:
```env
MONGO_URI=mongodb://localhost:27017/
DB_NAME=manchester_seals
FLASK_DEBUG=True
PORT=5100
```

For MongoDB Atlas:
```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
```

---

## 🐳 Docker Deployment

### Start Services
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f api
```

---

## 📊 Inserting Sample Data

### Option 1: Using Python Script
```bash
python3 insert_sample_data.py
```

### Option 2: Using Docker
```bash
docker exec manchester_seals_db mongosh manchester_seals << 'EOF'
db.roster.insertMany([
  {name: "John Doe", position: "Manager", department: "Operations", email: "john@example.com"},
  {name: "Jane Smith", position: "Developer", department: "Engineering", email: "jane@example.com"}
]);
EOF
```

### Option 3: Using Make
```bash
make sample-data
```

---

## 🧪 Testing

### Run Unit Tests
```bash
make test
# or
python -m pytest test_app.py -v
```

### Test API Endpoints
```bash
# Health check
curl http://localhost:5100/api/health

# Get roster data
curl http://localhost:5100/api/roster

# Get with pagination (extended version)
curl "http://localhost:5100/api/roster?page=1&limit=5"

# Search (extended version)
curl "http://localhost:5100/api/roster?search=john"
```

---

## 🛠️ Make Commands

```bash
make help               # Show all commands
make setup              # Complete setup (venv + install + config)
make install            # Install dependencies
make run                # Run basic version
make run-extended       # Run extended version
make test               # Run unit tests
make docker-up          # Start Docker Compose
make docker-down        # Stop Docker Compose
make docker-logs        # View Docker logs
make clean              # Clean cache files
make health             # Check API health
make sample-data        # Insert sample data
```

---

## 📁 Project Structure

```
manchester-seals-python-webservice/
├── app.py                      # Basic Flask application
├── app_extended.py             # Extended version with CRUD
├── config.py                   # Configuration management
├── test_app.py                 # Unit tests
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Docker Compose configuration
├── Makefile                    # Convenient commands
├── .env.example                # Environment template
├── .env                        # Your configuration
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

---

## 🔍 Troubleshooting

### Port Already in Use
If port 5100 is in use, change it in `.env`:
```env
PORT=5200
```

And update `docker-compose.yml`:
```yaml
ports:
  - "5200:5000"
```

### MongoDB Connection Failed
**Check if MongoDB is running:**
```bash
docker-compose ps
```

**For Docker:**
```bash
docker-compose restart mongodb
```

**For local MongoDB:**
```bash
# macOS
brew services start mongodb-community

# Linux
sudo systemctl start mongod
```

### API Returning Empty Data
1. **Check MongoDB has data:**
   ```bash
   docker exec manchester_seals_db mongosh manchester_seals --eval 'db.roster.countDocuments({})'
   ```

2. **Restart API:**
   ```bash
   docker-compose restart api
   ```

3. **Insert sample data:**
   ```bash
   python3 insert_sample_data.py
   ```

### Module Not Found Errors
```bash
pip install -r requirements.txt
```

---

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Docker Container
```bash
docker build -t manchester-seals-api .
docker run -p 5100:5000 manchester-seals-api
```

### Docker Compose (Recommended)
```bash
docker-compose up -d
```

### Cloud Platforms
- **Heroku:** `git push heroku main`
- **AWS:** Elastic Beanstalk or ECS
- **GCP:** Cloud Run
- **Azure:** App Service

---

## 🧩 Dependencies

- Flask 3.0.0
- pymongo 4.6.0
- python-dotenv 1.0.0
- pytest 7.4.3 (dev)

---

## 📝 API Response Examples

### Health Check
```json
{
  "status": "healthy",
  "service": "Manchester Seals API"
}
```

### Get Roster
```json
{
  "success": true,
  "count": 10,
  "data": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "name": "John Doe",
      "position": "Manager",
      "department": "Operations",
      "email": "john.doe@example.com",
      "salary": 85000,
      "hire_date": "2020-01-15"
    }
  ]
}
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `make test`
5. Submit a pull request

---

## 📄 License

This project is open source and available under the MIT License.

---

## 📞 Support

For issues or questions:
1. Check this README
2. Review the code comments
3. Check Docker logs: `docker-compose logs api`
4. Verify MongoDB: `docker exec manchester_seals_db mongosh`

---

## 🎉 Quick Reference

| Task | Command |
|------|---------|
| Start API | `make run` or `docker-compose up -d` |
| Stop API | `docker-compose down` |
| Test API | `curl http://localhost:5100/api/health` |
| Insert data | `python3 insert_sample_data.py` |
| Run tests | `make test` |
| View logs | `docker-compose logs -f api` |
| Clean up | `make clean` |

---

**Your Manchester Seals Python Webservice is ready!** 🚀

Start with: `make setup && make run`

Then visit: `http://localhost:5100/api/roster`

