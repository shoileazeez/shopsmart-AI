# ShopSmart AI

![System Design](https://img.shields.io/badge/System-Design-blue?style=flat-square)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)

> **AI-Powered E-commerce Platform** | Intelligent Product Discovery & Real-time Chat Commerce

Revolutionizing online shopping with **semantic search**, **AI-driven product recommendations**, and **real-time intelligent chat commerce**.

---

## 📋 Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Problem & Solution](#problem--solution)
* [Architecture](#architecture)
* [Core Components](#core-components)
* [Tech Stack](#tech-stack)
* [Getting Started](#getting-started)
* [Development](#development)
* [Contributing](#contributing)

---

## 👀 Overview

ShopSmart AI is a **next-generation e-commerce platform** that leverages artificial intelligence to transform how customers discover and purchase products. By combining semantic search, intelligent chatbots, and personalized recommendations, we're building the future of online retail.

✨ **Key Benefits:**

* 🔍 **Semantic Search**: Find products using natural language descriptions
* 💬 **AI Chat Commerce**: Real-time product guidance and purchase assistance
* 🎯 **Personalized Recommendations**: Smart product suggestions based on behavior
* ⚡ **Real-time Inventory**: Live stock updates and instant notifications

---

## 🚀 Features

### Core Pages

* **Home Dashboard** - Personalized shopping experience with trending products
* **Product Discovery** - Advanced semantic search with filters and sorting
* **Product Details** - Rich media gallery, specifications, reviews, and AI insights
* **Shopping Cart** - Persistent, real-time cart management
* **Checkout Flow** - Secure payment integration (Paystack/Stripe)
* **Order History** - Track orders with real-time status updates
* **User Profile** - Account management and preferences

### AI-Powered Capabilities

* **Semantic Image Search** - Find products by uploading images
* **Intelligent Chat Assistant** - 24/7 shopping assistance via AI chatbot
* **Product Recommendations** - Personalized suggestions using embeddings
* **Smart Inventory Search** - Natural language product discovery
* **Real-time Chat Commerce** - Purchase products directly through conversation using SSE

---

## 🎯 Problem & Solution

### The Problem

Traditional e-commerce platforms force users to:

* Navigate complex category hierarchies
* Perform multiple searches to find the right product
* Wait for human support for product questions
* Scroll through dozens of irrelevant results

### Our Solution

ShopSmart AI solves this by:

* **Natural Language Understanding** - Describe what you want, not search terms
* **Visual Search** - Upload an image to find similar products instantly
* **AI Assistant** - Get instant answers and recommendations 24/7
* **Smart Ranking** - See most relevant products first, powered by AI

---

## 🏗️ Architecture (Modular Monolith)

```
┌─────────────────────────────────────────────────────────────┐
│                       Modular Monolith                      │
│                 (Django + Clean Module Boundaries)          │
│                                                             │
│  ┌──────────────┬──────────────┬──────────────┬──────────┐ │
│  │  User Module │ Product Mod. │ Order Mod.   │ AI/Chat  │ │
│  └──────────────┴──────────────┴──────────────┴──────────┘ │
│  Each module contains:                                      │
│   • models/                                                │
│   • repositories/  (ORM logic)                              │
│   • services/       (Business logic)                        │
│   • signals/        (Django Signals for communication)      │
│   • api/            (DRF Views & Routers)                   │
└─────────────────────────────────────┬─────────────────────┘
                                      │ (HTTP / SSE)
                    ┌─────────────────▼──────────────────┐
                    │      Next.js Frontend (TailwindCSS) │
                    │       Google AI SDK (Gemini)        │
                    └─────────────────┬──────────────────┘
                                      │
       ┌──────────────────────────────┼─────────────────────────────┐
       │                              │                             │
   ┌───▼────────┐   ┌──────────────┐  ┌───────────────┐            │
   │ PostgreSQL │   │ Redis Cache  │  │ Object Storage │            │
   │ + pgvector │   │ (sessions +  │  │ (Appwrite)     │            │
   │            │   │ Celery tasks)│  │                │            │
   └────────────┘   └──────────────┘  └───────────────┘            │

   ┌─────────────────────────────────────────────────────────┐   │
   │                   AI Layer                               │   │
   │           Google Gemini + Embeddings                     │   │
   └─────────────────────────────────────────────────────────┘   │
```

---

## 🔧 Core Components

### 1. **Frontend (Next.js + TailwindCSS + Google AI SDK)**

* App Router
* Server Actions
* Google Gemini for LLM responses
* Google Embeddings API for semantic search
* SSE (Server-Sent Events) for real-time chat

### 2. **Django Modular Monolith Backend**

* Each domain is a fully isolated module
* Django Signals for inter-module communication
* Separate service & repository layers

### 3. **Database Layer**

* PostgreSQL + pgvector for semantic search

### 4. **Cache & Background Tasks**

* Redis for session cache
* Celery for asynchronous tasks

### 5. **Storage**

* Appwrite bucket for images & media

---

## 💻 Tech Stack

### Frontend

* **Next.js 15+**
* **TailwindCSS**
* **Google AI SDK**
* **SSE** for real-time events

### Backend

* **Django 4.2+**
* **Django REST Framework**
* **PostgreSQL + pgvector**
* **Redis** (cache + Celery tasks)

### AI/ML

* **Google Gemini** (LLM)
* **Google Embeddings** (vectors)

---

## 🚀 Getting Started

### Backend Setup

```bash
git clone https://github.com/shoileazeez/shopsmart-AI.git
cd shopsmart-AI
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## 🤝 Contributing

PRs are welcome! Follow conventional commits & ensure tests pass.

---

## 📄 License

MIT License — free to use and modify.

---

**By Abdulazeez Shoile**

