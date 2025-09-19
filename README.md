(al-mohasseb POS – SaaS Multi-Tenant Backend
A scalable, multi-tenant Point-of-Sale (POS) backend built with Django and Django REST Framework. Tailored for restaurants, cafés, and supermarkets in the Gulf region (Kuwait, Saudi Arabia, UAE). The platform manages tenant-specific databases, authentication, product and sales modules, and integrates with services like WhatsApp and thermal printers.

🚀 Features
Database-per-tenant architecture (PostgreSQL)
JWT + Session-based authentication
Dynamic Role-Based Access Control (RBAC)
Sales (POS), Inventory, Purchases and Expenses modules
Live Kitchen Order Management
Invoice generation (PDF) with thermal receipt printing
Meta WhatsApp Cloud API integration
Tenant onboarding and system provisioning

🛠️ Tech Stack
Backend: Django, Django REST Framework
Auth: djangorestframework-simplejwt, session auth
DB: PostgreSQL via django-tenants
PDF: WeasyPrint or xhtml2pdf
Printing: ESC/POS
Messaging: Meta WhatsApp Cloud API

🏗️ Multi-Tenant Architecture
This project uses django-tenants to keep each tenant in a dedicated schema:

public schema: contains shared apps such as authentication and subscription
{tenant_schema}: isolates tenant data (sales, products, etc.)
Each tenant therefore has its own PostgreSQL schema, users, products and reports.

Roles & Permissions
The system distinguishes between SaaS-level administrators ("Almohasseb" admins) and per-client roles:

SaaS admin – full access across all clients/tenants
Tenant admin – manages a single tenant's data
Sales – handles POS transactions
Delivery – manages delivery orders
Kitchen – handles kitchen order display
Listing all clients/tenants via the GET /api/tenants/ endpoint requires SaaS admin privileges.

🧩 API Endpoints Overview
✅ Login as SaaS Admin
Endpoint: POST /api/saas/login/

Request Body:

{
  "email": "example@ex.com",
  "password": "admin123"
}
Response:

{
    "token": {
        "refresh": "<refresh_token>",
        "access": "<access_token>"
    },
    "msg": "SaaS login successful"
}
Use this access token in all further requests:

Authorization: Bearer <jwt_token>

Base Domains
| Module | Base URL | Notes |
| --- | --- | --- |
| SaaS control plane | https://api.almohasseb.example.com/ | Hosts SaaS admin and provisioning APIs |
| Tenant runtime | https://<tenant-subdomain>.almohasseb.example.com/ | Tenant-specific schema + APIs |
| Local development | http://<schema-or-english-name>.localhost:<port>/ | Map hostnames in /etc/hosts for dev |


Authentication & Session Management
| Method | Endpoint | Description |
| --- | --- | --- |
| POST | /api/auth/login/ | Authenticate a tenant user and issue JWT + session cookie |
| POST | /api/auth/logout/ | Invalidate the refresh token / session for the active tenant user |
| GET | /api/auth/me/ | Retrieve the current tenant user's profile and permissions |


Example Request (tenant login):

POST /api/auth/login/
Content-Type: application/json

{
  "email": "sales@tenant.com",
  "password": "password123"
}

Example Response:

{
  "token": {
    "access": "<access>",
    "refresh": "<refresh>"
  },
  "user": {
    "id": 8,
    "name": "Sales Agent",
    "role": "sales",
    "permissions": ["pos.create-order", "chat.send-message"]
  }
}

User & Staff Management (Tenant scope)
| Method | Endpoint | Description |
| --- | --- | --- |
| GET | /api/users/ | List all active staff members for the current tenant |
| POST | /api/users/ | Create a new tenant staff user (manager, cashier, delivery, etc.) |
| GET | /api/users/<id>/ | Retrieve a single staff member by ID |
| PUT | /api/users/<id>/ | Update the staff member (role, status, branch assignments) |
| DELETE | /api/users/<id>/ | Archive/remove the staff member from the tenant |


Example Request (create tenant staff user):

POST /api/users/
Authorization: Bearer <access>
Content-Type: application/json

{
  "email": "kitchen@tenant.com",
  "password": "StrongPass!",
  "full_name": "Kitchen Display",
  "role": "kitchen",
  "phone": "+966500000000"
}

Example Response:

{
  "id": 21,
  "email": "kitchen@tenant.com",
  "full_name": "Kitchen Display",
  "role": "kitchen",
  "is_active": true,
  "created_at": "2024-10-09T11:15:23Z"
}

Customer Management
| Method | Endpoint | Description |
| --- | --- | --- |
| GET | /api/customers/ | List customers assigned to the tenant with search & pagination |
| POST | /api/customers/ | Create a new customer with contact info and meta tags |
| GET | /api/customers/<id>/ | Retrieve customer profile, tags, latest assignment |
| PUT | /api/customers/<id>/ | Update customer name, phone, notes (sales role permitted) |
| DELETE | /api/customers/<id>/ | Delete/archive a customer (admin or manager role) |
| GET | /api/customers/<id>/assignments/ | List historical salesperson assignments for this customer |
| GET | /api/customers/<id>/messages/ | Return the threaded WhatsApp/SMS messages for the customer |


Example Request (create customer):

POST /api/customers/
Authorization: Bearer <access>
Content-Type: application/json

{
  "name": "Fatima Ali",
  "phone": "+971500123456",
  "notes": "Prefers evening deliveries",
  "tags": ["VIP", "WhatsApp"],
  "assigned_to": 12
}

Example Response:

{
  "id": 44,
  "name": "Fatima Ali",
  "phone": "+971500123456",
  "notes": "Prefers evening deliveries",
  "tags": ["VIP", "WhatsApp"],
  "assigned_to": {
    "id": 12,
    "name": "Ahmed Saleh"
  },
  "created_at": "2024-10-09T11:20:41Z"
}

Assignment Management
| Method | Endpoint | Description |
| --- | --- | --- |
| POST | /api/assignments/ | Assign a salesperson or delivery agent to a customer thread |
| GET | /api/assignments/ | List all active assignments with filters (customer, user, status) |


Example Request (assign sales user):

POST /api/assignments/
Authorization: Bearer <access>
Content-Type: application/json

{
  "customer": 44,
  "user": 12,
  "note": "Transferred from inbound queue"
}

Example Response:

{
  "id": 87,
  "customer": {
    "id": 44,
    "name": "Fatima Ali"
  },
  "user": {
    "id": 12,
    "name": "Ahmed Saleh",
    "role": "sales"
  },
  "note": "Transferred from inbound queue",
  "assigned_at": "2024-10-09T11:22:03Z",
  "status": "active"
}

Messaging
| Method | Endpoint | Description |
| --- | --- | --- |
| GET | /api/messages/ | List inbound/outbound messages for all customers (paginated) |
| POST | /api/messages/ | Send a new outbound message via WhatsApp Cloud API |
| GET | /api/messages/<id>/ | Retrieve a specific message payload and delivery status |
| GET | /api/customers/<id>/messages/ | Convenience endpoint for one customer's message history |


Example Request (send message):

POST /api/messages/
Authorization: Bearer <access>
Content-Type: application/json

{
  "customer": 44,
  "type": "text",
  "text": {
    "body": "مرحبا! طلبك جاهز للتوصيل."
  },
  "attachments": []
}

Example Response:

{
  "id": "wamid.HBgLNzg...",
  "customer": 44,
  "direction": "out",
  "type": "text",
  "text": {
    "body": "مرحبا! طلبك جاهز للتوصيل."
  },
  "status": "sent",
  "timestamp": "2024-10-09T11:23:10Z",
  "sent_via": "whatsapp"
}

Webhook for Meta WhatsApp API
| Method | Endpoint | Description |
| --- | --- | --- |
| GET | /webhook/ | Meta webhook verification challenge (hub.verify_token) |
| POST | /webhook/ | Receive inbound WhatsApp events and broadcast to websockets |


Example Verification (GET /webhook/):

/webhook/?hub.mode=subscribe&hub.verify_token=<token>&hub.challenge=12345

Response: 200 OK with body "12345" when VERIFY_TOKEN matches.

Example Payload (POST /webhook/):

{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "123456",
      "changes": [
        {
          "value": {
            "contacts": [{"wa_id": "971500123456", "profile": {"name": "Fatima"}}],
            "messages": [
              {
                "from": "971500123456",
                "id": "wamid.HBgLNzg...",
                "timestamp": "1728463321",
                "type": "text",
                "text": {"body": "Hello"}
              }
            ]
          }
        }
      ]
    }
  ]
}

WebSocket (Real-Time Chat)
| Method | Endpoint | Description |
| --- | --- | --- |
| GET | ws://<host>/ws/chat/<conversation_id>/ | Subscribe to real-time message events for the conversation |


Example: ws://pos.localhost:8000/ws/chat/971500123456/

**Example message broadcast**

{
  "type": "message:new",
  "conversation_id": "971500123456",
  "message": {
    "id": "wamid.HBgLNzg...",
    "direction": "in",
    "type": "text",
    "text": "مرحبا",
    "timestamp": "1728463321",
    "status": "delivered",
    "sender": {"wa_id": "971500123456"}
  }
}

📚 SaaS Admin Endpoints
| Method | Endpoint | Description |
| --- | --- | --- |
| POST | /api/saas/login/ | Login SaaS admin and obtain access/refresh tokens |
| POST | /api/saas/logout/ | Revoke the active SaaS session (requires Authorization header) |
| GET | /api/saas/me/ | Get current SaaS admin profile (name, email, role) |
| POST | /api/saas/users/ | Add new SaaS admin user (email, password, role) |
| GET | /api/saas/users/ | List all SaaS admin users with pagination |
| GET | /api/saas/users/<id>/ | Retrieve SaaS admin user by ID |
| PUT | /api/saas/users/<id>/ | Update SaaS admin user details by ID |
| DELETE | /api/saas/users/<id>/ | Delete SaaS admin user by ID |
| POST | /token/refresh/ | Use refresh token to obtain a new access token |
| POST | /api/saas/addtenantusers/ | Create a tenant (company) manager user during onboarding |
| POST | /ten/tenants/ | Add tenant (company) record and auto-provision schema |
| GET | /ten/tenants/ | List tenants (companies) managed by SaaS admin |
| GET | /ten/tenants/<id>/ | Retrieve tenant details by SaaS admin |
| PUT | /ten/tenants/<id>/ | Update tenant (company) data by SaaS admin |
| PATCH | /ten/tenants/<id>/ | Partially update tenant configuration (status, modules) |
| DELETE | /ten/tenants/<id>/ | Delete tenant (company) by SaaS admin |
| GET | /ten/clients/ | List client contacts associated with tenants |
| POST | /ten/clients/ | Create client contact for a tenant |
| GET | /ten/clients/<id>/ | Retrieve client contact by SaaS admin |
| PUT | /ten/clients/<id>/ | Update client contact info by SaaS admin |
| PATCH | /ten/clients/<id>/ | Partially update client contact info |
| DELETE | /ten/clients/<id>/ | Delete client contact by SaaS admin |
| GET | /ten/domains/ | List configured tenant domains/subdomains |
| POST | /ten/domains/ | Create tenant domain mapping (domain + tenant schema) |


Example Request (create SaaS admin user):

POST /api/saas/users/
Authorization: Bearer <access>
Content-Type: application/json

{
  "email": "ops@almohasseb.com",
  "password": "ChangeMe!2024",
  "full_name": "Operations Lead",
  "role": "super_admin",
  "phone": "+96550000000"
}

Example Response:

{
  "id": 5,
  "email": "ops@almohasseb.com",
  "full_name": "Operations Lead",
  "role": "super_admin",
  "is_active": true,
  "created_at": "2024-10-09T10:55:00Z"
}

🧾 Create a New Client (Tenant)
✅ Endpoint
URL: POST /ten/tenants/

Headers:

Authorization: Bearer <jwt_token>
Content-Type: application/json
Request JSON:

    {
        "arabic_name": "اخري",
        "english_name": "Other",
        "commercial_record": "1234567890",
        "subdomain": "other",
        "subscription_price": "767.23",
        "currency": "SAR",
        "start_date": "2025-08-01",
        "end_date": "2030-01-01",
        "on_trial": true,
        "image": null,
        "is_active": true,
        "no_users": 5,
        "modules_enabled": {
            "kitchen": false,
            "delivery": false,
            "inventory": true
        },
        "activity_type": "other",
        "no_branches": 1,
        "billing": {
            "contact_name": "Yara Harby",
            "phone": "+96555555555",
            "email": "billing@other.com"
        },
        "branches": [
            {
                "name": "Main Branch",
                "city": "Riyadh",
                "phone": "+966500111222",
                "is_default": true
            }
        ]
    }

Note:

subdomain is used to generate schema_name (must be lowercase, alphanumeric, start with a letter).
You can optionally include branches as a nested list.
Response:

{
  "id": 18,
  "arabic_name": "اخري",
  "english_name": "Other",
  "schema_name": "other",
  "domain": "other.almohasseb.example.com",
  "is_active": true,
  "on_trial": true,
  "modules_enabled": {
    "kitchen": false,
    "delivery": false,
    "inventory": true
  },
  "created_at": "2024-10-09T11:01:32Z"
}

create client of the tenant
✅ Endpoint
URL: POST /ten/clients/

Request Body:

{
    "tenant": 18,
    "arabic_name": "يوسف",
    "english_name": "Youssef",
    "email": "yaraharby22@gmail.com",
    "phone": "+966512345678",
    "role": "manager"
}

Response:

{
  "id": 92,
  "tenant": 18,
  "arabic_name": "يوسف",
  "english_name": "Youssef",
  "email": "yaraharby22@gmail.com",
  "phone": "+966512345678",
  "role": "manager",
  "status": "active"
}

🔒 Permissions
All /ten/ endpoints are protected with IsAdminUser.
Only users with user_type='saas_admin' and a valid JWT token can access tenant management routes.
Tenant-scoped /api/* routes require a valid tenant host header and JWT for that tenant.

✅ Example Flow in Postman
POST /api/saas/login/ → copy access token
POST /ten/tenants/ → create tenants
POST /ten/clients/ → add client to that company (tenant)
POST /api/saas/addtenantusers/ → invite tenant manager
Switch to https://<tenant>.localhost:<port>/ context → log in as tenant user
Use tenant-level /api/customers/, /api/messages/, etc.

manager endpoints
✅ Endpoint
note --> each endpoint starts with http://<schema name or english name of company>.localhost:<the port>/
like this http://ymy.localhost:<the port>/tenuser/tenantusers/ except the login or logout endpoints

Tenant Authentication & User Management
| Method | Endpoint | Description |
| --- | --- | --- |
| POST | /tenuser/login/ | Login as a tenant manager or staff member |
| POST | /tenuser/tenantusers/ | Create a new user for a tenant |
| GET | /tenuser/tenantusers/ | List users for a tenant |
| GET | /tenuser/tenantusers/<id>/ | Retrieve a tenant user |
| PUT | /tenuser/tenantusers/<id>/ | Update a tenant user |
| PATCH | /tenuser/tenantusers/<id>/ | Partially update a tenant user |
| DELETE | /tenuser/tenantusers/<id>/ | Delete/disable a tenant user |


Example Request (tenant login):

POST /tenuser/login/
Content-Type: application/json

{
  "tenant": "other",
  "email": "manager@other.com",
  "password": "Manager123"
}

Response:

{
  "token": {
    "access": "<access>",
    "refresh": "<refresh>"
  },
  "user": {
    "id": 2,
    "name": "Tenant Manager",
    "role": "tenant_admin"
  }
}

Branch Management
| Method | Endpoint | Description |
| --- | --- | --- |
| POST | /tenuser/branches/ | Create a new branch for a tenant |
| GET | /tenuser/branches/ | List branches for a tenant |
| GET | /tenuser/branches/<id>/ | Retrieve branch details |
| PUT | /tenuser/branches/<id>/ | Update branch details |
| PATCH | /tenuser/branches/<id>/ | Partially update branch data |
| DELETE | /tenuser/branches/<id>/ | Delete a branch |


Example Request (create branch):

POST /tenuser/branches/
Authorization: Bearer <access>
Content-Type: application/json

{
  "name": "Mall Branch",
  "city": "Dubai",
  "phone": "+971500222333",
  "is_default": false
}

Response:

{
  "id": 7,
  "name": "Mall Branch",
  "city": "Dubai",
  "phone": "+971500222333",
  "is_default": false,
  "created_at": "2024-10-09T11:05:17Z"
}

Operational APIs (tenant)
| Method | Endpoint | Description |
| --- | --- | --- |
| GET | /api/customers/ | List tenant customers (same as above but scoped per tenant) |
| POST | /api/customers/ | Create tenant customer |
| PUT | /api/customers/<id>/ | Update customer info / sales notes |
| DELETE | /api/customers/<id>/ | Archive customer record |
| GET | /api/assignments/ | List assignments inside tenant workspace |
| POST | /api/assignments/ | Create new assignment inside tenant workspace |
| GET | /api/messages/ | List messages inside tenant workspace |
| POST | /api/messages/ | Send outbound message |
| GET | /api/messages/<id>/ | Retrieve specific message record |
| GET | /api/customers/<id>/messages/ | Conversation history for one customer |
| GET | /api/customers/<id>/assignments/ | Assignment history for one customer |


Example Request (tenant send message):

POST http://other.localhost:8000/api/messages/
Authorization: Bearer <access>
Content-Type: application/json

{
  "customer": 44,
  "type": "interactive",
  "interactive": {
    "type": "button",
    "body": "هل تريد متابعة الطلب؟",
    "buttons": [
      {"id": "confirm", "title": "نعم"},
      {"id": "support", "title": "تواصل مع الدعم"}
    ]
  }
}

Response:

{
  "id": "wamid.HBgLNzgu...",
  "customer": 44,
  "direction": "out",
  "type": "interactive",
  "interactive": {
    "type": "button",
    "body": "هل تريد متابعة الطلب؟",
    "buttons": [
      {"id": "confirm", "title": "نعم"},
      {"id": "support", "title": "تواصل مع الدعم"}
    ]
  },
  "status": "sent",
  "timestamp": "2024-10-09T11:30:45Z"
}
