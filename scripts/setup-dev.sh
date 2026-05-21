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
echo "3. Start frontend: cd frontend && npm run dev"
echo ""
echo "Visit http://localhost:3000 untuk see Tessera dashboard"
echo ""
echo "Verifikasi cepat (lint, tipe, pytest): dari root repo jalankan ./scripts/verify.sh"
echo "Verifikasi lebih berlapis (build Next produksi + compileall backend): ./scripts/verify-full.sh atau npm run verify:full"
