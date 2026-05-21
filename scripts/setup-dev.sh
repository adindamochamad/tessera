#!/bin/bash

# Tessera Development Setup Script
# Automatically setup development environment

set -e

echo "🚀 Tessera - Development Setup"
echo "================================"

# Check prerequisites
echo "✓ Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

echo "✓ Prerequisites met"

# Backend setup
echo ""
echo "📦 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✓ Backend setup complete"

# Demo app setup
echo ""
echo "📦 Setting up demo-app..."
cd ../demo-app
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -q -r requirements.txt
deactivate
echo "✓ Demo app setup complete"

# Frontend setup
echo ""
echo "📦 Setting up frontend..."
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
else
    echo "✓ Node modules already installed"
fi

echo "✓ Frontend setup complete"

# Environment configuration
cd ..
if [ ! -f ".env" ]; then
    echo ""
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your credentials before running"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file dengan your Google Cloud dan MongoDB credentials"
echo "2. Start backend: cd backend && source venv/bin/activate && uvicorn app.api.main:app --reload"
echo "3. Start demo-app: cd demo-app && source venv/bin/activate && uvicorn app.main:aplikasi --reload --port 8081"
echo "4. Seed Atlas (jika URI sudah di .env): python3 scripts/seed_mongodb_demo.py"
echo "5. Start frontend: cd frontend && npm run dev"
echo "6. Infra GCP/Atlas: lihat docs/INFRA_DAY1.md"
echo ""
echo "Visit http://localhost:3000 untuk see Tessera dashboard"
echo ""
echo "Verifikasi cepat (lint, tipe, pytest): dari root repo jalankan ./scripts/verify.sh"
echo "Verifikasi lebih berlapis (build Next produksi + compileall backend): ./scripts/verify-full.sh atau npm run verify:full"
