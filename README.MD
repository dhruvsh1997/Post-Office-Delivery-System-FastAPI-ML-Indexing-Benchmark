# 📬 Post Office Delivery System – FastAPI + ML + Indexing Benchmark

This project is a **Post Office Delivery Backend System** built with **FastAPI**, a **Random Forest ML model** for delivery time prediction, and **PostgreSQL** for a normalized relational database. It demonstrates database indexing performance and machine learning integration in a simplified, beginner-friendly way.

---

## 🚀 Features

- 🧠 **ML-Powered Delivery Time Prediction**: Uses Random Forest to predict delivery times based on traffic, weather, and other factors.
- 📊 **Normalized ERD**: Third Normal Form (3NF) database schema with PostOffice, DeliveryPerson, and Delivery tables.
- ⚙️ **CRUD Operations**: Create and retrieve delivery records via API endpoints.
- 🧪 **Indexing Performance Comparison**: Compare query performance with and without indexes on the `delivery_status` column.
- 📈 **Data Population**: Populate the database with realistic fake data for testing.
- 🐘 **PostgreSQL with SQLAlchemy**: Efficient database operations using SQLAlchemy ORM.

---

## 🗂️ Project Structure

```
post_delivery_app/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic schemas for API validation
│   ├── ml/
│   │   ├── train_model.py   # Random Forest model training
│   │   ├── delivery_time_model.pkl  # Saved ML model
│   └── utils/
│       ├── data_spammer.py  # Data population script
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

---

## 📊 Entity Relationship Diagram (ERD)

The database is in 3rd Normal Form (3NF) with three main tables and a single index for demonstration.

```mermaid
erDiagram
    PostOffice ||--o{ DeliveryPerson : post_office_id
    PostOffice ||--o{ Delivery : post_office_id
    DeliveryPerson ||--o{ Delivery : delivery_person_id

    PostOffice {
        int id PK
        string branch_code UK
        string name
        string address
        float latitude
        float longitude
    }
    DeliveryPerson {
        int id PK
        string employee_id UK
        string name
        int age
        float rating
        int post_office_id FK
    }
    Delivery {
        int id PK
        string delivery_id UK
        int post_office_id FK
        int delivery_person_id FK
        float distance_km
        float estimated_delivery_time
        float actual_delivery_time
        string delivery_status "Indexed: idx_delivery_status"
        string traffic_level
        string weather_description
        string package_type
        string vehicle_type
        float temperature
        float humidity
        float precipitation
        datetime created_at
    }
```

**Relationships**:
- `PostOffice` to `DeliveryPerson`: One-to-Many (`post_office_id`).
- `PostOffice` to `Delivery`: One-to-Many (`post_office_id`).
- `DeliveryPerson` to `Delivery`: One-to-Many (`delivery_person_id`).

**Indexes**:
- Primary Keys: `id` in each table.
- Unique Keys: `branch_code` (PostOffice), `employee_id` (DeliveryPerson), `delivery_id` (Delivery).
- Custom Index: `idx_delivery_status` on `Delivery.delivery_status`.

---

## 🔄 API Flow Diagram

```mermaid
graph TD
    A[Client/User] -->|POST /deliveries| B[Create Delivery with ML Prediction]
    A -->|GET /deliveries/with-index| C[Query Deliveries with Index]
    A -->|GET /deliveries/without-index| D[Query Deliveries without Index]
    B --> E[Delivery Table]
    C & D --> E[Delivery Table]
```

---

## 📌 Core API Endpoints

### 🚚 Delivery Creation
- **POST /deliveries**
  - Creates a new delivery with a predicted delivery time using the Random Forest model.
  - Input: `post_office_id`, `delivery_person_id`, `distance_km`, `traffic_level`, `weather_description`, etc.
  - Output: Delivery ID and success message.

### 🧪 Indexing Performance Test
- **GET /deliveries/with-index?status=delivered**
  - Fetches deliveries filtered by status using the `idx_delivery_status` index.
  - Returns execution time to show indexing benefits.
- **GET /deliveries/without-index?status=delivered**
  - Fetches deliveries without using the index (drops it temporarily).
  - Returns execution time for comparison.

**Create the Index Manually**:
```sql
CREATE INDEX idx_delivery_status ON deliveries(delivery_status);
```

### 🧨 Data Population
- The `populate_data` function (in `data_spammer.py`) inserts sample data:
  - 10 PostOffices
  - 20 DeliveryPersons
  - 100+ Deliveries (configurable)
- Call this function manually or create a custom endpoint to trigger it.

---

## 🔍 How Indexing Works
- **Indexed Column**: `delivery_status` (e.g., "pending", "delivered").
- **Without Index**: PostgreSQL scans the entire `deliveries` table (sequential scan), which is slow for large datasets.
- **With Index**: Uses the `idx_delivery_status` index to quickly locate relevant rows (index scan).
- **Analyze Query Performance**:
  ```sql
  EXPLAIN ANALYZE SELECT * FROM deliveries WHERE delivery_status = 'delivered';
  ```

**Example Performance** (with 1,000 deliveries):
| Traffic Level | Rows   | Indexed? | Time Taken |
|---------------|--------|----------|------------|
| Delivered     | 1,000  | ❌ No    | ~0.5s      |
| Delivered     | 1,000  | ✅ Yes   | ~0.05s     |

---

## ⚙️ How to Run Locally

### 📦 Install Dependencies
```bash
pip install -r requirements.txt
```

**requirements.txt**:
```
fastapi==0.115.0
uvicorn==0.30.6
sqlalchemy==2.0.31
psycopg2-binary==2.9.9
pandas==2.2.2
scikit-learn==1.5.1
faker==28.1.0
joblib==1.4.2
```

### 🐘 Set Up PostgreSQL
1. Install PostgreSQL locally or use a Docker container:
   ```bash
   docker run -d --name postgres -p 5432:5432 -e POSTGRES_DB=postdeliverydb -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=password postgres:latest
   ```
2. Update the database URL in `main.py`:
   ```python
   engine = create_engine("postgresql://admin:password@localhost:5432/postdeliverydb")
   ```

### ⚙️ Train the ML Model
```bash
python app/ml/train_model.py
```
This generates `delivery_time_model.pkl` for predictions.

### ▶️ Start the FastAPI Server
```bash
uvicorn app.main:app --reload
```

### 🌐 Access API Docs
Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API documentation.

### 🧪 Populate Data
1. Modify `main.py` to call `populate_data(db, num_records=1000)` after database creation.
2. Alternatively, create a `POST /spam` endpoint:
   ```python
   @app.post("/spam")
   def spam_data(num_records: int = 1000, db: Session = Depends(get_db)):
       populate_data(db, num_records)
       return {"message": f"Inserted {num_records} records"}
   ```

### 🧪 Test Indexing
1. Populate the database with 1,000+ deliveries.
2. Compare `/deliveries/with-index?status=delivered` vs. `/deliveries/without-index?status=delivered`.
3. Check the `execution_time_ms` in the responses to see the indexing benefit.

---

## 📈 Example Usage

### Create a Delivery
```bash
curl -X POST "http://127.0.0.1:8000/deliveries" \
-H "Content-Type: application/json" \
-d '{
    "post_office_id": 1,
    "delivery_person_id": 1,
    "distance_km": 10.0,
    "traffic_level": "Medium",
    "weather_description": "Clear",
    "package_type": "document",
    "vehicle_type": "bike",
    "delivery_person_age": 30,
    "delivery_person_rating": 4.5,
    "temperature": 25.0,
    "humidity": 60.0,
    "precipitation": 0.0
}'
```

### Compare Indexing Performance
```bash
curl "http://127.0.0.1:8000/deliveries/with-index?status=delivered"
curl "http://127.0.0.1:8000/deliveries/without-index?status=delivered"
```

---

## 📌 Future Improvements
- Add composite indexes (e.g., on `delivery_status` and `created_at`).
- Implement full CRUD for `PostOffice` and `DeliveryPerson`.
- Add a frontend with Chart.js to visualize indexing performance.
- Include additional tables (e.g., `Customer`, `Package`) from the original ERD.
- Use Docker Compose for easier setup.
- Add GitHub Actions for CI/CD.

---

## 🧩 Want Extras?
Let me know if you need:
- `docker-compose.yml` for PostgreSQL.
- GitHub Actions workflow for CI/CD.
- A frontend to visualize performance metrics.
- Additional tables or endpoints from the original code.

---

## 🙌 Contributions
Pull requests and issues are welcome! Let's make learning about indexing and ML fun 🚀.

---

## 📘 License
MIT License © 2025