# MEAL System - نظام المتابعة والتقييم والمساءلة والتعلم

> Monitoring, Evaluation, Accountability & Learning System for Humanitarian Organizations in Yemen

## نظرة عامة | Overview

نظام MEAL متكامل مصمم خصيصاً للمنظمات الإنسانية العاملة في اليمن. يوفر النظام أدوات شاملة لإدارة المشاريع، متابعة المؤشرات، إدارة المستفيدين، آليات المساءلة، وتوثيق الدروس المستفادة.

A comprehensive MEAL system designed for humanitarian organizations operating in Yemen. Provides tools for project management, indicator tracking, beneficiary management, accountability mechanisms, and lessons learned documentation.

## الوحدات | Modules

### MEAL Core
- **لوحة المعلومات (Dashboard)** - KPIs, charts, real-time statistics
- **المتابعة والتقييم (Monitoring)** - Indicator tracking with IPTT (Indicator Performance Tracking Table)
- **المساءلة (Accountability)** - Complaint & Feedback Mechanism (CFM) with multi-channel support
- **التعلم (Learning)** - Lessons learned documentation and sharing
- **خطة MEAL** - MEAL planning per project with M, E, A, L approaches
- **الإطار المنطقي (LogFrame)** - Theory of Change / Results Framework

### Program Management
- **المشاريع (Projects)** - Multi-sector project management with budget tracking
- **المستفيدين (Beneficiaries)** - Registration, duplicate detection, vulnerability scoring
- **الأنشطة (Activities)** - Activity tracking linked to projects
- **الزيارات الميدانية (Field Visits)** - Field monitoring visits with findings/recommendations

### Operations
- **المالية (Finance)** - Grant management, transactions, burn rate analysis
- **التحويلات النقدية (Cash/CVA)** - Cash & Voucher Assistance with hawala/mobile money
- **المخازن (Inventory)** - Warehouse management with low-stock alerts
- **الموارد البشرية (HR)** - Employee management, leave tracking

### Tools
- **جمع البيانات (Data Collection)** - Mobile forms with KoBoToolbox integration ready
- **التقارير (Reports)** - 6 report types (project, beneficiary, indicator, financial, distribution, accountability)
- **المخاطر (Risks)** - Risk register with 5x5 matrix visualization
- **الوثائق (Documents)** - Document management system
- **الإشعارات (Notifications)** - In-app notification system
- **المزامنة (Offline Sync)** - Offline-first data sync for field operations

## التقنيات | Tech Stack

### Backend
- **FastAPI** (Python 3.12) - High-performance async API
- **SQLAlchemy 2.0** - ORM with SQLite (upgradeable to PostgreSQL)
- **JWT Authentication** - Role-based access control (7 roles)
- **Pydantic** - Data validation

### Frontend
- **React 18** with Vite
- **Tailwind CSS** - RTL-first Arabic UI
- **Recharts** - Data visualization
- **Lucide Icons** - Clean icon system
- **Axios** - API client with JWT interceptors

## التثبيت والتشغيل | Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```
API available at: http://localhost:8000
API docs: http://localhost:8000/docs

### Frontend (Development)
```bash
cd frontend
npm install
npm run dev
```
Frontend at: http://localhost:5173

### Full Build (Production)
```bash
cd frontend && npm run build
cp -r dist ../backend/frontend_dist
cd ../backend && python main.py
```
Full app at: http://localhost:8000

## بيانات تجريبية | Demo Credentials

| User | Password | Role |
|------|----------|------|
| admin | admin123 | مدير النظام |
| meal_officer | pass123 | مسؤول MEAL |
| manager1 | pass123 | مدير برامج |
| field1 | pass123 | موظف ميداني |
| finance1 | pass123 | مالية |
| hr1 | pass123 | موارد بشرية |

### Seed Data
- 8 projects across health, food security, WASH, education, protection, shelter, nutrition
- 150 beneficiaries across 12 Yemeni governorates
- 12 indicators with 12 months of measurements
- 6 grants from WHO, WFP, UNICEF, ECHO, USAID, KSRelief
- 30 employees across 6 departments
- 5 warehouses with inventory
- 25 complaints/feedback entries
- 15 field visits, 12 risk entries, 10 lessons learned

## البنية | Architecture

```
MEAL/
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── requirements.txt
│   └── app/
│       ├── config.py           # Settings
│       ├── database.py         # SQLAlchemy engine
│       ├── auth.py             # JWT authentication
│       ├── models.py           # 18+ SQLAlchemy models
│       ├── seed.py             # Yemen-context seed data
│       └── routers/
│           ├── auth.py         # Login, current user
│           ├── dashboard.py    # KPIs and charts
│           ├── beneficiaries.py
│           ├── projects.py
│           ├── monitoring.py   # Indicators, IPTT
│           ├── accountability.py # CFM
│           ├── learning.py
│           ├── finance.py
│           ├── hr.py
│           ├── inventory.py
│           ├── cash.py
│           ├── data_collection.py
│           ├── reports.py
│           ├── documents.py
│           ├── field_visits.py
│           ├── risks.py
│           ├── logframe.py
│           ├── meal_plan.py
│           ├── notifications.py
│           └── offline_sync.py
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       ├── index.css
│       ├── contexts/AuthContext.jsx
│       ├── services/api.js
│       ├── components/
│       │   ├── Layout.jsx
│       │   ├── StatCard.jsx
│       │   ├── DataTable.jsx
│       │   ├── Modal.jsx
│       │   └── StatusBadge.jsx
│       └── pages/
│           ├── Login.jsx
│           ├── Dashboard.jsx
│           ├── Beneficiaries.jsx
│           ├── Projects.jsx
│           ├── Monitoring.jsx
│           ├── Indicators.jsx
│           ├── Accountability.jsx
│           ├── Learning.jsx
│           ├── MEALPlan.jsx
│           ├── LogFrame.jsx
│           ├── FieldVisits.jsx
│           ├── Finance.jsx
│           ├── Cash.jsx
│           ├── Inventory.jsx
│           ├── HR.jsx
│           ├── DataCollection.jsx
│           ├── Reports.jsx
│           ├── Documents.jsx
│           ├── Risks.jsx
│           └── Activities.jsx
└── README.md
```

## خصائص للسياق اليمني | Yemen-Specific Features

- **Offline-First Architecture** - Sync queue for intermittent connectivity
- **Arabic-First UI** - Full RTL support with Tajawal font
- **Multiple Cash Transfer Methods** - Hawala, mobile money, bank, cash-in-hand
- **Vulnerability Scoring** - 1-10 scale for beneficiary prioritization
- **IDP Tracking** - Internal displacement status tracking
- **Multi-Governorate Coverage** - All 12 major governorates
- **CHS Compliance** - Core Humanitarian Standard aligned CFM
- **Multi-Channel CFM** - Phone, WhatsApp, SMS, suggestion box, in-person

## API Endpoints

20+ router modules providing 100+ REST endpoints. Full interactive documentation available at `/docs` when running the server.
