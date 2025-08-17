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
| GET    | `/api/saas/me/`         | Get current SaaS admin info(see profile)  |
| POST   | `/api/saas/users/`      | add new Saas admin             |
| GET    | `/api/saas/users/`      | List all SaaS admin users      |
| GET    | `/api/saas/users/<id>/` | Retrieve SaaS admin user by ID |
| PUT    | `/api/saas/users/<id>/` | Update SaaS admin user by ID   |
| DELETE | `/api/saas/users/<id>/` | Delete SaaS admin user by ID   |
| POST   | `/token/refresh/`       | use refresh to get acces token |
| POST   | `/api/saas/addtenantusers/`| create Tenant (company) user(manger) |
| POST   | `/ten/tenants/`| add  Tenant (company)|
| GET   | `/ten/tenants/`| list  Tenant (company)|
| GET   | `/ten/tenants/<id>/`    | Retrieve clientby saas|
| PUT    | `/ten/teanant/<id>/`    | Update Tenant (client) by saas |
| DELETE | `/ten/tenants/<id>/`    | Delete Tenant (client) by saas |
| PATCH  | `/ten/tenants/<id>`     | Update Tenant (client) by saas |
| GET   | `/ten/clients/`         | list client        |
| POST   | `/ten/clients/`         | create client       |
| GET   | `/ten/clients/<id>/`    | Retrieve clientby saas|
| PUT    | `/ten/clients/<id>/`    | Update Tenant (client) by saas |
| DELETE | `/ten/clients/<id>/`    | Delete Tenant (client) by saas |
| PATCH  | `/ten/clients/<id>`     | Update Tenant (client) by saas |
| POST   | `/ten/domains/`    | create and list domains|


---

## 🧾 Create a New Client (Tenant)

### ✅ Endpoint

**URL:** `POST /ten/tenants/`

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
## create client of the tenant 
### ✅ Endpoint
**URL:** `POST /ten/clients/`

**Request Body:**

```json
{
    "tenant":2,
    "arabic_name":"يوسف",
    "english_name":"youssef",
    "email":"yaraharby22@gmail.com",
    "phone":48327483
}
```




## 🔒 Permissions

* All `/ten/` endpoints are protected with `IsAdminUser`.
* Only users with `user_type='saas_admin'` and a valid JWT token can access tenant management routes.

---

## ✅ Example Flow in Postman

1. `POST /api/saas/login/` → copy access token
2. `POST /ten/tenants/` → create tenants
3. `POST /ten/clients/` → add client to that company(tenant)

---
## manager endpoints

### ✅ Endpoint
### note --> each endpoint starts with `http://<schema name or english name of company>.localhost:<the port>/`
### like this `http://ymy.localhost:<the port>/tenuser/tenantusers/` except the login or logout endpoints
| Method | Endpoint                | Description                    |
| ------ | ----------------------- | ------------------------------ |
| POST | `tenuser/login/`          | login as a manager or any other tenant user            |
| POST | `tenuser/tenantusers/`| create a new user for a tenant|
| GIT | `tenuser/tenantusers/`| list users for a tenant|
| GIT | `tenuser/tenantusers//<id>/`|retrive one user for a tenant|
| PUT | `tenuser/tenantusers/<id>/`| update a user for a tenant|
| DELETE | `tenuser/tenantusers/<id>/`| delete a user for a tenant|
| PATCH | `tenuser/tenantusers/<id>/`| update a user for a tenant|
| POST | `tenuser/branches/`| create a new branch for a tenant|
| GET | `tenuser/branches/`| list branches for a tenant|
| GET | `tenuser/branches/<id>/`| retrive a branch for a tenant|
| PUT | `tenuser/branches/<id>/`| update a branch for a tenant|
| DELETE | `tenuser/branches/<id>/`| delete a branch for a tenant|
| PATCH | `tenuser/branches/<id>/`| update a branch for a tenant|











