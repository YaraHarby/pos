# al-mohasseb POS – SaaS Multi-Tenant Backend

A scalable, multi-tenant Point-of-Sale (POS) backend built with Django and Django REST Framework. Tailored for restaurants, cafés, and supermarkets in the Gulf region (Kuwait, Saudi Arabia, UAE). The platform manages tenant-specific databases, authentication, product and sales modules, and integrates with services like WhatsApp and thermal printers.

## 🚀 Features
- Database-per-tenant architecture (PostgreSQL)
- JWT + Session-based authentication
- Dynamic Role-Based Access Control (RBAC)
- Sales (POS), Inventory, Purchases and Expenses modules
- Live Kitchen Order Management
- Invoice generation (PDF) with thermal receipt printing
- Meta WhatsApp Cloud API integration
- Tenant onboarding and system provisioning

## 🛠️ Tech Stack
- **Backend:** Django, Django REST Framework
- **Auth:** djangorestframework-simplejwt, session auth
- **DB:** PostgreSQL via `django-tenants`
- **PDF:** WeasyPrint or xhtml2pdf
- **Printing:** ESC/POS
- **Messaging:** Meta WhatsApp Cloud API

## 🏗️ Multi-Tenant Architecture
This project uses `django-tenants` to keep each tenant in a dedicated schema:

- **public** schema: contains shared apps such as authentication and subscription
- **{tenant_schema}**: isolates tenant data (sales, products, etc.)

Each tenant therefore has its own PostgreSQL schema, users, products and reports.

## Roles & Permissions
The system distinguishes between **SaaS-level** administrators ("Almohasseb" admins) and
per-client roles:

- SaaS admin – full access across all clients/tenants
- Tenant admin – manages a single tenant's data
- Sales – handles POS transactions
- Delivery – manages delivery orders
- Kitchen – handles kitchen order display

Listing all clients/tenants via the `GET /api/tenants/` endpoint requires SaaS admin privileges.



## 🧩 API Endpoints Overview





### ✅ Login as SaaS Admin

**Endpoint:** `POST /api/saas/login/`

**Request Body:**

```json
{
  "email": "example@ex.com",
  "password": "admin123"
}
```

**Response:**

```json
{
    "token": {
        "refresh": "",
        "access": ""
    },
    "msg": "SaaS login successful"
}
```

**Use this access token in all further requests:**

```
Authorization: Bearer <jwt_token>
```

---

## 📚 SaaS Admin Endpoints

| Method | Endpoint                | Description                    |
| ------ | ----------------------- | ------------------------------ |
| POST   | `/api/saas/login/`      | Login SaaS admin               |
| POST   | `/api/saas/logout/`     | Logout SaaS admin              |
| GET    | `/api/saas/me/`         | Get current SaaS admin info    |
| POST   | `/api/saas/users/`      | add new Saas admin             |
| GET    | `/api/saas/users/`      | List all SaaS admin users      |
| GET    | `/api/saas/users/<id>/` | Retrieve SaaS admin user by ID |
| PUT    | `/api/saas/users/<id>/` | Update SaaS admin user by ID   |
| DELETE | `/api/saas/users/<id>/` | Delete SaaS admin user by ID   |
| POST   | `/token/refresh/`       | use refresh to get acces token |
| POST   | `/api/saas/addtenantusers/`| create Tenant (client) user |
---

## 🧾 Create a New Client (Tenant)

### ✅ Endpoint

**URL:** `POST /ten/clients/`

**Headers:**

* `Authorization: Bearer <jwt_token>`
* `Content-Type: application/json`

**Request JSON:**

```json
    {
        "id": 1,
        "arabic_name": "اخري",
        "english_name": "other",
        "Commercial_Record": 123,
        "subdomain": "other",
        "Subscription_Price": "767.23",
        "Currency": "SAR",
        "Start_Date": "2025-08-01",
        "End_Date": "2030-01-01",
        "on_trial": true,
        "image": null,
        "is_active": true,
        "no_users": 1,
        "modules_enabled": {
            "kitchen": false,
            "reports": false,
            "sellers": true,
            "Delivery": false
        },
        "Activity_Type": "other",
        "no_branches": 1
    }
```

**Note:**

* `subdomain` is used to generate `schema_name` (must be lowercase, alphanumeric, start with a letter).
* You can optionally include `branches` as a nested list.



**Response:**

```json
{
  "id": 8,
  "name": "My Supermarket",
  // ... other fields
}
```

---

## 🏬 Create Branch for an Existing Client

### ✅ Endpoint

**URL:** `POST /ten/branches/`

**Request Body:**

```json
{
  "name": "Supermarket Main Branch",
  "tenant": 8,
  "contact_email": "branch@supermarket.com",
  "contact_phone": "999999999"
}
```

**Response:**

```json
{
  "id": 1,
  "name": "Supermarket Main Branch",
  "tenant": 8,
  "contact_email": "branch@supermarket.com",
  "contact_phone": "999999999"
}
```

---

## 🔒 Permissions

* All `/ten/` endpoints are protected with `IsSaasAdmin`.
* Only users with `user_type='saas_admin'` and a valid JWT token can access tenant management routes.

---

## ✅ Example Flow in Postman

1. `POST /api/saas/login/` → copy token
2. `POST /ten/clients/` → create client
3. `POST /ten/branches/` → add branches to that client

---

## 🧾 Client and Branch Management Endpoints

This section lists all endpoints for managing clients (tenants) and branches in the Al-Mohasseb SaaS POS backend.

---

### 🏢 Client Endpoints

| Method | Endpoint             | Description                  |
| ------ | -------------------- | ---------------------------- |
| GET    | `/ten/clients/`      | List all clients             |
| POST   | `/ten/clients/`      | Create a new client (tenant) |
| GET    | `/ten/clients/<id>/` | Retrieve specific client     |
| PATCH  | `/ten/clients/<id>/` | Partially update a client    |
| PUT    | `/ten/clients/<id>/` | Fully update a client        |
| DELETE | `/ten/clients/<id>/` | Delete a client              |

---

### 🏬 Branch Endpoints

| Method | Endpoint              | Description               |
| ------ | --------------------- | ------------------------- |
| GET    | `/ten/branches/`      | List all branches         |
| POST   | `/ten/branches/`      | Create a new branch       |
| GET    | `/ten/branches/<id>/` | Retrieve specific branch  |
| PATCH  | `/ten/branches/<id>/` | Partially update a branch |
| PUT    | `/ten/branches/<id>/` | Fully update a branch     |
| DELETE | `/ten/branches/<id>/` | Delete a branch           |

---

### 🔒 Authentication

All endpoints listed above are protected and require:

* SaaS Admin JWT token in the header:

```
Authorization: Bearer <your_token>
```

---

### 🌐 Notes

* Branches require a valid `tenant` ID on creation.
* When updating, only allowed fields need to be sent.
* Deleting a client will also delete its branches.

---







### 🧑‍🤝‍🧑 User & Role APIs
| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| GET | /api/users/ | List users |
| POST | /api/users/ | Create user |
| GET | /api/users/{id}/ | Get user details |
| PATCH | /api/users/{id}/ | Update user |
| POST | /api/roles/ | Create role |
| GET | /api/roles/ | List roles |
| POST | /api/roles/assign/ | Assign role to user + branch |

### 🛒 POS / Sales APIs
| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| POST | /api/sales/ | Create new sale |
| GET | /api/sales/ | List sales |
| GET | /api/sales/{id}/ | Sale details |
| POST | /api/sales/{id}/invoice/ | Generate/send invoice PDF |
| POST | /api/sales/{id}/whatsapp/ | Send invoice via WhatsApp |

### 📦 Product APIs
| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| GET | /api/products/ | List products |
| POST | /api/products/ | Add product |
| PATCH | /api/products/{id}/ | Update product |
| DELETE | /api/products/{id}/ | Delete product |
| GET | /api/products/search/ | Search product (barcode/name) |

### 📥 Purchases & Expenses
| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| POST | /api/purchases/ | Record purchase |
| POST | /api/expenses/ | Log new expense |
| GET | /api/purchases/ | List purchases |
| GET | /api/expenses/ | List expenses |

### 🍽️ Kitchen Orders
| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| GET | /api/kitchen-orders/ | List active orders |
| PATCH | /api/kitchen-orders/{id}/ | Update status (in-progress/done) |

### 📊 Reports
| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| GET | /api/reports/sales/ | Filterable sales report |
| GET | /api/reports/purchases/ | Filterable purchases report |
| GET | /api/reports/expenses/ | Expense report |
| GET | /api/reports/summary/ | Daily/Weekly balance overview |
| POST | /api/reports/export/ | Export reports to PDF/Excel |

### 🧾 Invoices
| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| GET | /api/invoices/{id}/view/ | Render invoice (PDF) |
| GET | /api/invoices/{id}/download/ | Download invoice |
| POST | /api/invoices/{id}/print/ | Trigger thermal printer |
| POST | /api/invoices/{id}/whatsapp/ | Send via WhatsApp |


## 📁 Project Structure

```text
root/
├── backend/                     # Django backend (multi-tenant, DRF)
│   ├── backend/               # Django project folder (contains settings, wsgi, asgi)
│   ├── tenants/                # Schema routing, subdomain middleware (django-tenants)
│   ├── custom_auth/            # JWT/session login, user roles, permissions
│   ├── clients/                # Subscription plans, module activation, client industry setup
│   ├── products/               # Product inventory, categories, low-stock alerts
│   ├── sales/                  # POS transactions, cart, invoice trigger
│   ├── kitchen/                # Live kitchen orders, status update
│   ├── finances/               # Purchases and expenses, supplier tracking
│   ├── invoices/               # PDF generation, ESC/POS printing, WhatsApp sending
│   ├── reports/                # Custom reports: sales, purchases, summaries
│   ├── scripts/                # CLI scripts: tenant creation, provisioning
│   ├──.env.template               # Example environment config for dev
│   └──manage.py
│
├── frontend/                   # React frontend (modular by client roles)
│   ├── src/
│   │   ├── components/         # Shared UI components
│   │   ├── pages/              # Pages per module (POS, Kitchen, Admin, etc.)
│   │   └── utils/              # Frontend helpers, API configs
│   └── public/
│
└── README.md
```






## 🧪 Dev Setup
```bash
git clone https://github.com/your-org/pos-backend.git
cd pos-backend
py -3.11 -m venv venv
./venv/scripts/activate
pip install -r requirements.txt

# Set up initial public schema and superuser
python manage.py migrate_schemas --shared
python manage.py createsuperuser --schema=public

# Create a new client tenant
python manage.py create_tenant

# Install and run the frontend
cd frontend
npm install
npm run dev

# Access the React frontend at http://localhost:5173/login and authenticate
# with your Django credentials. After login you can manage clients.

```

## 📓 Future Enhancements
- Offline POS support (via local PWA cache)
- QR code for invoice scanning
- Loyalty points module
- Delivery GPS tracking


---

