# 💳 Credit Approval System

This project is a **Django REST API** for managing customer credit and loan approvals —  
fully containerized using **Docker**, integrated with **PostgreSQL**, and **deployed live on Render**.

---

## 🚀 Live Project Links

- **🌐 Live Backend:** [https://credit-approval-system-26fb.onrender.com/](https://credit-approval-system-26fb.onrender.com/)
- **🐘 PostgreSQL Database:** Hosted on Render Cloud (connected live)
- **🧠 Background Task (Celery):** Handles Excel data ingestion for customers and loans

---

## ⚙️ Tech Stack

| Component | Technology |
|------------|-------------|
| Language | Python 3.10 |
| Framework | Django 5.2.7 + Django REST Framework |
| Database | PostgreSQL 14 (Render Cloud) |
| Background Tasks | Celery |
| Containerization | Docker + Docker Compose |
| Deployment | Render |
| Dev Tools | VS Code, pgAdmin 4, Postman |

---

## 🧩 Key Features

✅ Register a new customer with automatic credit limit calculation  
✅ Create and approve loan requests based on eligibility rules  
✅ View all loans for a specific customer  
✅ Calculate EMIs using compound interest  
✅ Ingest Excel data (`customer_data.xlsx`, `loan_data.xlsx`) via Celery background worker  
✅ Fully containerized and deployed on the cloud  
✅ Django Admin interface for managing all customers and loans  

---

## 📚 Data Flow Summary

1️⃣ Excel files → `tasks.py` (Celery) → PostgreSQL Database  
2️⃣ APIs handle:
   - `/register` → add new customers  
   - `/check-eligibility` → compute credit score  
   - `/create-loan` → approve/reject based on limits  
   - `/view-loan` & `/view-loans` → show approved details  
3️⃣ Admin Dashboard → visualizes all data live  

---

## 🔗 API Endpoints

| Method | Endpoint | Description | Example Link |
|--------|-----------|--------------|---------------|
| **GET** | `/` | Root endpoint — API health check | [Live](https://credit-approval-system-26fb.onrender.com/) |
| **POST** | `/api/v1/register/` | Register a new customer | [Register Customer](https://credit-approval-system-26fb.onrender.com/api/v1/register/) |
| **POST** | `/api/v1/check-eligibility/` | Check loan eligibility for a customer | [Check Eligibility](https://credit-approval-system-26fb.onrender.com/api/v1/check-eligibility/) |
| **POST** | `/api/v1/create-loan/` | Create a new loan for an eligible customer | [Create Loan](https://credit-approval-system-26fb.onrender.com/api/v1/create-loan/) |
| **GET** | `/api/v1/view-loan/<loan_id>/` | View details of a specific loan | [View Loan Example](https://credit-approval-system-26fb.onrender.com/api/v1/view-loan/1/) |
| **GET** | `/api/v1/view-loans/<customer_id>/` | View all loans for a given customer | [View All Loans](https://credit-approval-system-26fb.onrender.com/api/v1/view-loans/10/) |
| **Admin Panel** | `/admin/` | Manage Customers & Loans | [Admin Login](https://credit-approval-system-26fb.onrender.com/admin/) |

---

## 🧮 Credit Score Logic (Eligibility Rules)

- If **past EMIs are paid on time → +score**
- If **total active loan amount ≤ approved limit → +score**
- If **total EMIs exceed 50% of salary → reject**
- Based on credit score:
  - >50 → approve normally  
  - 30–50 → approve, interest ≥12%  
  - 10–30 → approve, interest ≥16%  
  - <10 → reject loan  

---

## 🧰 Steps to Run Locally

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/shivani324/credit_approval_system.git
cd credit_approval_system
```

### 2️⃣ Build Docker Image
```bash
docker build -t credit_approval_system .
```

### 3️⃣ Run Containers
```bash
docker-compose up
```

### 4️⃣ Access Locally
Open your browser → [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🐳 Deployment Details

- **Docker Hub Repository:** `shivani324/credit_approval_system`
- **Render Backend:** [https://credit-approval-system-26fb.onrender.com/](https://credit-approval-system-26fb.onrender.com/)
- **Database:** Render-hosted PostgreSQL instance
- **Background Task:** Celery worker for data ingestion

---

##  Example Request — `/api/v1/register/`

### **Request**
```json
{
  "first_name": "Aarav",
  "last_name": "Sharma",
  "age": 30,
  "monthly_income": 60000,
  "phone_number": "9876543210"
}
```

### **Response**
```json
{
  "customer_id": 301,
  "name": "Aarav Sharma",
  "age": 30,
  "monthly_income": 60000,
  "approved_limit": 2160000,
  "phone_number": "9876543210"
}
```

---

##  Admin Dashboard Overview

- **Customers Table:** Displays name, salary, approved limit, current debt  
- **Loans Table:** Displays loan amount, interest rate, tenure, EMI  
- Accessible at → [https://credit-approval-system-26fb.onrender.com/admin/](https://credit-approval-system-26fb.onrender.com/admin/)  

---

##  Author

**Shivani Shahi**  
🎓 B.Tech in Electrical Engineering | Haldia Institute of Technology  
📧 Email: shivanishahi324@gmail.com  
🔗 LinkedIn: [https://linkedin.com/in/shivani-shahi](https://linkedin.com/in/shivani-shahi)  
🐙 GitHub: [https://github.com/shivani324](https://github.com/shivani324)

---

##  Summary

This backend automates credit approval using Django REST, PostgreSQL, and Celery.  
It ingests customer & loan data, computes credit scores, approves loans, and provides complete API endpoints for all operations.  
Deployed and live with full Docker and PostgreSQL integration.  

**Fully functional |  Cloud Deployed |  PostgreSQL |  Dockerized |  Ready for Production**
