# ShopSmart AI

[![System Design](https://img.shields.io/badge/System-Design-blue?style=flat-square)](./ARCHITECTURE.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

> **AI-Powered E-commerce Platform** | Intelligent Product Discovery & Real-time Chat Commerce

Revolutionizing online shopping with **semantic search**, **AI-driven product recommendations**, and **real-time intelligent chat commerce**.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Problem & Solution](#problem--solution)
- [Architecture](#architecture)
- [Core Components](#core-components)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Development](#development)
- [Roadmap](#roadmap)
- [Contributing](#contributing)

---

## 👀 Overview

ShopSmart AI is a **next-generation e-commerce platform** that leverages artificial intelligence to transform how customers discover and purchase products. By combining semantic search, intelligent chatbots, and personalized recommendations, we're building the future of online retail.

✨ **Key Benefits:**
- 🔍 **Semantic Search**: Find products using natural language descriptions
- 💬 **AI Chat Commerce**: Real-time product guidance and purchase assistance
- 🎯 **Personalized Recommendations**: Smart product suggestions based on behavior
- ⚡ **Real-time Inventory**: Live stock updates and instant notifications

---

## 🚀 Features

### Core Pages
- **Home Dashboard** - Personalized shopping experience with trending products
- **Product Discovery** - Advanced semantic search with filters and sorting
- **Product Details** - Rich media gallery, specifications, reviews, and AI insights
- **Shopping Cart** - Persistent, real-time cart management
- **Checkout Flow** - Secure payment integration (Paystack/Stripe)
- **Order History** - Track orders with real-time status updates
- **User Profile** - Account management and preferences

### AI-Powered Capabilities
- **Semantic Image Search** - Find products by uploading images
- **Intelligent Chat Assistant** - 24/7 shopping assistance via AI chatbot
- **Product Recommendations** - Personalized suggestions using embeddings
- **Smart Inventory Search** - Natural language product discovery
- **Real-time Chat Commerce** - Purchase products directly through conversation

---

## 🎯 Problem & Solution

### The Problem
Traditional e-commerce platforms force users to:
- Navigate complex category hierarchies
- Perform multiple searches to find the right product
- Wait for human support for product questions
- Scroll through dozens of irrelevant results

### Our Solution
ShopSmart AI solves this by:
- **Natural Language Understanding** - Describe what you want, not search terms
- **Visual Search** - Upload an image to find similar products instantly
- **AI Assistant** - Get instant answers and recommendations 24/7
- **Smart Ranking** - See most relevant products first, powered by AI

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Frontend Layer                              │
│           (Next.js 14, React 18, MUI, Framer Motion)            │
│                                                                  │
│  ┌────────────┬──────────────┬──────────────┬──────────────┐    │
│  │  Dashboard │   Search     │   Chat       │   Checkout   │    │
│  └────────────┴──────────────┴──────────────┴──────────────┘    │
└─────────────────────────────────────┬──────────────────────────┘
                                      │ (HTTP/WebSocket)
                    ┌─────────────────▼──────────────────┐
                    │     Kong API Gateway              │
                    │ (Authentication, Rate Limiting)   │
                    └─────────────────┬──────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
    ┌───▼───┐  ┌──────────┐  ┌──────▼──────┐  ┌───────────┐       │
    │ User  │  │ Product  │  │ AI Service  │  │  Payment  │       │
    │Service│  │ Service  │  │  (LLM)      │  │  Service  │       │
    └───────┘  └──────────┘  └─────────────┘  └───────────┘       │
        │           │              │               │                │
    ┌───▼───────────▼──────────────▼───────────────▼──────┐        │
    │           PostgreSQL + pgvector                     │        │
    │      (Catalog, Users, Orders, Embeddings)          │        │
    └──────────────────────────────────────────────────────┘        │
        │                                                            │
    ┌───▼──────────────┐      ┌──────────────────────┐             │
    │  Redis Cache     │      │  redis pub/sub        │             │
    │  (Sessions)      │      │  (Event Queue)       │             │
    └──────────────────┘      └──────────────────────┘             │
        │                                                            │
    ┌───▼──────────────────────────────────────────┐               │
    │     Object Storage (S3-compatible) + CDN     │               │
    │         (Images, Media, Documents)           │               │
    └────────────────────────────────────────────────┘              │
                                                                    │
    ┌────────────────────────────────────────────────┐             │
    │         AI/ML Pipeline                         │             │
    │  (Embeddings, Semantic Search, Ranking)       │             │
    └────────────────────────────────────────────────┘             │
```

---

## 🔧 Core Components

### 1. **Frontend Service** (Next.js)
- Server-side rendering (SSR) for SEO
- WebSocket connections for real-time chat
- Responsive design with Material-UI
- Framer Motion animations
- Client-side state management

### 2. **API Gateway** (Kong)
- Centralized authentication & authorization
- Rate limiting and request validation
- API versioning and routing
- Request/response logging and monitoring

### 3. **User Service** (Django)
- User registration and authentication
- JWT token management
- User profile and preferences
- Wishlist and saved items

### 4. **Product Service** (Django)
- Product catalog management
- Category and tag organization
- Inventory tracking
- Product reviews and ratings

### 5. **AI Service** (Django + Python)
- LLM integration (Vercel AI, Google Gemini)
- Semantic search implementation
- Embedding generation and storage
- Chat conversation management
- Recommendation engine

### 6. **Order & Payment Service** (Django)
- Order creation and management
- Payment processing (Paystack, Stripe)
- Invoice generation
- Order tracking and history

### 7. **Notification Service** (Django)
- Email notifications
- SMS alerts
- Real-time WebSocket notifications
- Event-driven notifications

---

## 💻 Tech Stack

### Frontend
- **Framework**: Next.js 14+ with TypeScript
- **UI Library**: Material-UI (MUI) v5+
- **Animation**: Framer Motion
- **State Management**: Redux Toolkit / Zustand
- **HTTP Client**: Axios / Fetch API
- **Real-time**: WebSocket (Socket.io)

### Backend
- **Framework**: Django 4.2+ with Django REST Framework (DRF)
- **Database**: PostgreSQL 15+ with pgvector extension
- **Cache**: Redis 7+
- **Task Queue**: Celery with Redis broker
- **Real-time**: Django Channels with WebSocket support
- **Message Broker**: redis (optional, for event streaming)

### API & Infrastructure
- **API Gateway**: Kong 3.x
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Rate Limiting**: Redis-based
- **Containerization**: Docker & Docker Compose

### AI/ML
- **LLM Provider**: Vercel AI SDK + Google Gemini
- **Embeddings**: Google AI Embeddings / pgvector
- **Vector Store**: PostgreSQL pgvector extension
- **Search**: Semantic similarity matching

### Payment Processing
- **Primary**: Paystack API
- **Fallback**: Stripe API
- **Webhook Management**: django-webhook-manager

### Infrastructure & DevOps
- **Frontend Hosting**: Vercel
- **Backend Hosting**: Render
- **Database**: Managed PostgreSQL for AI and product service seperate DB for the rest
- **Storage**: Appwrite cloud storage
- **CDN**: Cloudflare or AWS CloudFront
- **CI/CD**: GitHub Actions

---

## 🚀 Getting Started

### Prerequisites

**Backend:**
- Python 3.10+
- PostgreSQL 15+
- Redis 7+
- Node.js 18+ (for frontend)

**Frontend:**
- Node.js 18+
- npm or yarn

### Installation

#### Backend Setup (Django)

```bash
# Clone the repository
git clone https://github.com/shoileazeez/shopsmart-AI.git
cd shopsmart-AI

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file and configure variables (see Environment Variables section)

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

#### Frontend Setup (Next.js)

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file (see Environment Variables section)

# Start development server
npm run dev

# Open http://localhost:3000
```

### Environment Variables

Create `.env` file in project root (backend):

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/shopsmart_db

# Redis
REDIS_URL=redis://localhost:6379

# Django
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT
JWT_SECRET=your-jwt-secret

# Payment (Paystack)
PAYSTACK_PUBLIC_KEY=your-paystack-public-key
PAYSTACK_SECRET_KEY=your-paystack-secret-key

# AI/LLM
GOOGLE_API_KEY=your-google-api-key

# Storage (S3)
appwrite_endpoint=your-appwrite-endpoint
appwrite_project_id=your-appwrite-project-id
appwrite_api_key=your-appwrite-api-key

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

Create `.env.local` file in `frontend` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
NEXT_PUBLIC_VERCEL_AI_API=your-api-endpoint
```

---

## 🔨 Development

### Running Services

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
python manage.py runserver

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Celery (background tasks)
celery -A config worker -l info

# Terminal 4: Redis (if not running as service)
redis-server
```

### Common Commands

```bash
# Backend
python manage.py migrate              # Run migrations
python manage.py createsuperuser      # Create admin user
python manage.py collectstatic        # Collect static files
python manage.py test                 # Run tests

# Frontend
npm run dev                           # Development server
npm run build                         # Production build
npm run lint                          # ESLint
npm test                              # Run tests
npm run format                        # Prettier formatting
```

### Testing

```bash
# Backend tests
pytest

# Frontend tests
npm test

# Coverage
pytest --cov=.
```

---

## 📅 Roadmap

### MVP (Weeks 1-2) ✅
- [x] User authentication & JWT
- [x] Basic product catalog
- [x] Shopping cart functionality
- [x] Order management
- [x] Paystack integration
- [x] Frontend with Next.js & MUI
- [x] Product search (basic text search)

### Phase 1: AI Services (Weeks 3-6)
- [ ] Semantic search implementation
- [ ] Embedding generation pipeline
- [ ] AI chatbot integration (Vercel AI + Google Gemini)
- [ ] Product recommendations engine
- [ ] Image search capability
- [ ] Chat commerce flow

### Phase 2: Advanced Features (Weeks 7-10)
- [ ] Event-driven architecture (Kafka)
- [ ] Real-time notifications
- [ ] Inventory management system
- [ ] Analytics dashboard
- [ ] Admin panel enhancements
- [ ] Performance optimization

### Future Enhancements
- [ ] Voice commerce integration
- [ ] AR product preview
- [ ] Machine learning-powered personalization
- [ ] Mobile app (React Native / Flutter)
- [ ] Marketplace for sellers
- [ ] Subscription management
- [ ] Multi-language support
- [ ] AI-powered fraud detection

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines
- Follow PEP 8 (Python) and ESLint (JavaScript) style guides
- Write tests for new features
- Update documentation accordingly
- Keep commits atomic and well-described

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 📞 Contact

- **Project Lead**: Shoileazeez
- **Email**: contact@shopsmart-ai.com
- **GitHub**: [@shoileazeez](https://github.com/shoileazeez)
- **Issues**: [GitHub Issues](https://github.com/shoileazeez/shopsmart-AI/issues)

---

## 🙏 Acknowledgments

- [Next.js](https://nextjs.org/) - React framework
- [Django](https://www.djangoproject.com/) - Web framework
- [Material-UI](https://mui.com/) - UI components
- [PostgreSQL](https://www.postgresql.org/) - Database
- [Vercel AI](https://sdk.vercel.ai/) - AI SDK
- [Paystack](https://paystack.com/) - Payment processing

---

**Made with ❤️ by the ShopSmart AI Team**
