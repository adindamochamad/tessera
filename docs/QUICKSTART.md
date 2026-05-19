# Tessera - Quick Start Guide

## Prerequisites

- Python 3.11+
- Node.js 18+
- Google Cloud account
- MongoDB Atlas account

## Installation

### Option 1: Automated Setup (Recommended)

```bash
# Clone repository
git clone https://github.com/[username]/tessera.git
cd tessera

# Run setup script
chmod +x scripts/setup-dev.sh
./scripts/setup-dev.sh

# Edit environment variables
nano .env  # or use your preferred editor
```

### Option 2: Manual Setup

#### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Frontend

```bash
cd frontend
npm install
```

## Configuration

Create `.env` file di root directory:

```bash
# Copy dari template
cp .env.example .env
```

Edit `.env` dengan your credentials:

```env
# Google Cloud
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=./path/to/service-account.json
VERTEX_AI_LOCATION=us-central1

# MongoDB
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/
MONGODB_DATABASE=tessera_demo
```

## Running Locally

### Terminal 1: Backend API

```bash
cd backend
source venv/bin/activate
uvicorn app.api.main:app --reload
```

Backend akan running di `http://localhost:8000`

### Terminal 2: Frontend

```bash
cd frontend
npm run dev
```

Frontend akan running di `http://localhost:3000`

## Testing

### Backend Tests

```bash
cd backend
source venv/bin/activate
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Common Issues

### Issue: Google Cloud Authentication Error

**Solution**: Ensure service account JSON file path adalah correct di `.env`

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/service-account.json
```

### Issue: MongoDB Connection Failed

**Solution**: Check MongoDB URI dan ensure IP address whitelisted di Atlas

### Issue: Port Already in Use

**Solution**: Change port di `.env`:

```env
API_PORT=8001  # Backend
```

For frontend, edit `package.json`:
```json
{
  "scripts": {
    "dev": "next dev -p 3001"
  }
}
```

## Development Workflow

1. **Create feature branch**
   ```bash
   git checkout -b feature/nama-feature
   ```

2. **Make changes**
   - Edit code
   - Add tests
   - Update documentation

3. **Test locally**
   ```bash
   pytest  # Backend
   npm test  # Frontend
   ```

4. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: deskripsi perubahan"
   ```

5. **Push dan create PR**
   ```bash
   git push origin feature/nama-feature
   ```

## Next Steps

- Read [ARCHITECTURE.md](docs/ARCHITECTURE.md) untuk understanding system design
- Check [CONTRIBUTING.md](CONTRIBUTING.md) untuk contribution guidelines
- Join GitHub Discussions untuk questions

## Support

- GitHub Issues: Report bugs
- GitHub Discussions: Ask questions
- Email: [Your email]

---

**Built with ❤️ for Google Cloud Rapid Agent Hackathon 2026**
