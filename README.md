
# 🛒 E-Commerce REST API (FastAPI Machine Test)

A high-performance, RESTful API for an E-commerce platform built with **FastAPI**, **SQLAlchemy**, and **Pydantic**. This application manages Categories and Products with a secure, scalable architecture.

> **Note:** In addition to the standard requirements, this implementation includes **API Key Authentication**, **Rate Limiting (Throttling)**, and **Global Exception Handling** to demonstrate advanced capabilities.

---

## 📋 Database Design Details

This section outlines the schema design, relationships, and constraints used to satisfy the assignment's RDBMS and ORM requirements.

### 1. Entity-Relationship (ER) Overview
The database consists of two primary entities with a **One-to-Many** relationship.

*   **Entity A:** `Category` (The "One" side)
*   **Entity B:** `Product` (The "Many" side)
*   **Logic:** A single Category can contain multiple Products, but a Product can belong to only one Category.

### 2. Detailed Schema Definition

#### Table: `categories`
This table stores the high-level classifications for products.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | **PRIMARY KEY**, Auto-Increment | Unique identifier for the category. |
| `name` | `String` (VARCHAR) | **UNIQUE**, **INDEXED**, Not Null | The name of the category (e.g., "Electronics"). Cannot be duplicated. |

#### Table: `products`
This table stores the individual items available for sale.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | **PRIMARY KEY**, Auto-Increment | Unique identifier for the product. |
| `name` | `String` (VARCHAR) | **INDEXED**, Not Null | The product name. Indexed for faster search performance. |
| `price` | `Float` | Not Null | The price of the product. |
| `category_id` | `Integer` | **FOREIGN KEY**, Not Null | Links to `categories(id)`. Enforces that a product must have a valid category. |

### 3. Relationships & Integrity

*   **Foreign Key Constraint:**
    *   The `category_id` column in the `products` table references the `id` column in the `categories` table.
    *   **Impact:** You cannot create a product with a `category_id` that does not exist in the categories table (Referential Integrity).

*   **Data Retrieval Strategy:**
    *   When fetching a single product via `GET /api/products/{id}`, the API performs a JOIN operation (via SQLAlchemy ORM relationship) to return the product details **embedded with** the full category object.

---

## ✨ Features

| Feature | Description | Status |
| :--- | :--- | :--- |
| **RESTful Architecture** | Standard HTTP methods (GET, POST, PUT, DELETE) with semantic URLs. | ✅ Completed |
| **Database ORM** | Full SQLAlchemy integration with automatic table creation. | ✅ Completed |
| **Relationships** | **One-to-Many** relationship between Categories and Products. | ✅ Completed |
| **Server-Side Pagination** | Efficient pagination for all listing endpoints (`?page=1&limit=10`). | ✅ Completed |
| **Data Validation** | Pydantic schemas for request/response validation. | ✅ Completed |
| **Security** | API Key protection for Write operations (POST, PUT, DELETE). | ✅ **Bonus** |
| **Throttling** | Rate limiting (20 req/min for Read, 5 req/min for Write). | ✅ **Bonus** |

---

## 🛠️ Installation Steps

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Prathameshsci369/-E-Commerce-REST-API-FastAPI-Machine-Test-.git
    cd fastapi_ecommerce
    ```

2.  **Create Virtual Environment** (Recommended)
    ```bash
    python3 -m venv venv
    
    # Activate on Linux/Mac
    source venv/bin/activate
    
    # Activate on Windows
    venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🚀 Running the Application

The application uses **SQLite** by default for immediate portability. To switch to **PostgreSQL**, simply change the `DATABASE_URL` in `app/database.py`.

### Start the Server

Run the following command in the terminal:

```bash
uvicorn app.main:app --reload
```

*   **Access API Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
*   **Access ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔐 Security & Usage

### Public Endpoints (No Key Required)
*   `GET /api/categories/`
*   `GET /api/products/`
*   `GET /api/categories/{id}`
*   `GET /api/products/{id}`

### Protected Endpoints (API Key Required)
*   `POST /api/categories/`
*   `POST /api/products/`
*   `PUT /api/categories/{id}`
*   `PUT /api/products/{id}`
*   `DELETE ...`

### How to use the API Key
1.  Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
2.  Click the **🔒 Authorize** button at the top right.
3.  Enter the API Key:
    ```text
    my-secret-token
    ```
4.  Click "Authorize" and close. You can now execute Write operations.

---

## 📚 API Endpoints Summary

### Categories
| Method | Endpoint | Description | Query Params |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/categories/` | List all categories | `page`, `limit` |
| `POST` | `/api/categories/` | Create a new category | - |
| `GET` | `/api/categories/{id}` | Get category by ID | - |
| `PUT` | `/api/categories/{id}` | Update category | - |
| `DELETE` | `/api/categories/{id}` | Delete category | - |

### Products
| Method | Endpoint | Description | Query Params |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/products/` | List all products (with pagination) | `page`, `limit` |
| `POST` | `/api/products/` | Create a new product | - |
| `GET` | `/api/products/{id}` | Get product by ID (Includes Category Info) | - |
| `PUT` | `/api/products/{id}` | Update product | - |
| `DELETE` | `/api/products/{id}` | Delete product | - |

---

## 🧪 Testing Throttling (Rate Limiting)
The API is protected against spam:
*   **Read Requests:** Limited to **20 requests/minute**.
*   **Write Requests:** Limited to **5 requests/minute**.

To test: Execute a `POST` request rapidly. After the 5th request in a minute, you will receive a `429 Too Many Requests` error.

---

## 📂 Project Structure
```text
/fastapi_ecommerce
├── app/
│   ├── __init__.py
│   ├── main.py           # Routes, Endpoints, & Logic
│   ├── database.py       # DB Configuration & Session
│   ├── models.py         # SQLAlchemy Tables
│   ├── schemas.py        # Pydantic Validation
│   └── security.py       # API Key & Rate Limiting
├── ecommerce.db          # SQLite Database (Auto-generated)
├── requirements.txt      # Python Dependencies
└── README.md            # This file
```

---

## 👨‍💻 Author
Built for Machine Test Submission.
```

This update provides the formal "Database Design Details" section requested in your submission requirements, explicitly listing columns, types, and constraints.
