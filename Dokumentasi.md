# 📦 Pinjemin

## 🚀 Instalasi & Setup

### 1. Clone Repository
```bash
git clone https://github.com/username/nama-repo.git
cd nama-repo
```
### 2. Buat dan Aktifkan Virtual Environment (Python)
```bash
# Buat venv
python -m venv venv

# Aktifkan (Windows)
venv\Scripts\activate

# Aktifkan (Mac/Linux)
source venv/bin/activate
```

### 3.  Install Dependencies Python dan Install Frontend
```bash
pip install -r requirements.txt
npm install
```

### 4. Menjalankan Aplikasi
```bash
uvicorn main:app --reload 
npm run start
```

# 📫 API Endpoint List

### **Base URL**
> http://localhost:5000/api

### 1. Recommend User
* Url: /recommend/user
* Method: Post
* Body: raw, json
  ```json
  { 
  "user_id": 9,
  "top_n": 5
  }
  ```

* Response Body :
  ```json
   {
    "recommendations": [
        {
            "product_id": 32255,
            "product_name": "Buku Hosit Enak-Enak Jajanan dan Street Food Populer Khas Pontianak (Vianney Lim)",
            "seller_id": 457,
            "product_rating": 4.9,
            "product_price": 67150
        },
        {
            "product_id": 32204,
            "product_name": "Buku Hingga Akhir Waktu (Brian Greene)",
            "seller_id": 457,
            "product_rating": 5,
            "product_price": 168300
        },
        {
            "product_id": 31799,
            "product_name": "Buku Educomics Plants Vs Zombies Bertahan Hidup di Alam",
            "seller_id": 457,
            "product_rating": 4.9,
            "product_price": 106250
        },
        {
            "product_id": 32697,
            "product_name": "Buku Lautan dan Dendamnya (Adib Izra Mirza)",
            "seller_id": 457,
            "product_rating": 5,
            "product_price": 115000
        },
        {
            "product_id": 32744,
            "product_name": "Buku Life Reset: Bertumbuh Dimulai Dari Sini (Senja Rindiani)",
            "seller_id": 457,
            "product_rating": 4.9,
            "product_price": 83300
        }
    ]
  }
   ```
 
### 2. Recommend Search
* Url: /recommend/search
* Method: Post
* Body: raw,json
  ```
  {
  "keyword": "novel",
  "top_n": 10
  }
  ```
* Response Body:
  ```json
   {
    "recommendations": [
        {
            "product_id": 33228,
            "product_name": "Buku Novel - Novel The School for Good and Evil 2: Dunia Tanpa Pangeran (2022)",
            "seller_id": 420,
            "product_rating": 5,
            "product_price": 142800
        },
        {
            "product_id": 33225,
            "product_name": "Buku Novel - Novel The School for Good and Evil 2: Dunia Tanpa Pangeran (2022)",
            "seller_id": 1471,
            "product_rating": 5,
            "product_price": 142800
        },
        {
            "product_id": 33224,
            "product_name": "Buku Novel - Novel The School for Good and Evil 2: Dunia Tanpa Pangeran (2022)",
            "seller_id": 882,
            "product_rating": 5,
            "product_price": 142800
        },
        {
            "product_id": 33229,
            "product_name": "Buku Novel - Novel The School for Good and Evil 2: Dunia Tanpa Pangeran (2022)",
            "seller_id": 457,
            "product_rating": 5,
            "product_price": 142800
        },
        {
            "product_id": 33226,
            "product_name": "Buku Novel - Novel The School for Good and Evil 2: Dunia Tanpa Pangeran (2022)",
            "seller_id": 2414,
            "product_rating": 5,
            "product_price": 142800
        },
        {
            "product_id": 33230,
            "product_name": "Buku Novel - Novel The School for Good and Evil 2: Dunia Tanpa Pangeran (2022)",
            "seller_id": 637,
            "product_rating": 5,
            "product_price": 142800
        },
        {
            "product_id": 33227,
            "product_name": "Buku Novel - Novel The School for Good and Evil 2: Dunia Tanpa Pangeran (2022)",
            "seller_id": 1557,
            "product_rating": 5,
            "product_price": 142800
        },
        {
            "product_id": 33222,
            "product_name": "Buku Novel - Novel The School for Good and Evil 2: Dunia Tanpa Pangeran (2022)",
            "seller_id": 2299,
            "product_rating": 5,
            "product_price": 142800
        },
        {
            "product_id": 33223,
            "product_name": "Buku Novel - Novel The School for Good and Evil 2: Dunia Tanpa Pangeran (2022)",
            "seller_id": 178,
            "product_rating": 5,
            "product_price": 142800
        },
        {
            "product_id": 313956,
            "product_name": "Novel Bulan - Tere Liye",
            "seller_id": 1139,
            "product_rating": 4.9,
            "product_price": 99750
        }
    ]
  }
  ```

### 3. Recommend Item
* Url: /recommend/item
* Method: Post
* Body: raw,json
  ```
  {
  "product_id": 30070,
  "top_n": 1
  }
  ```
* Response Body:
  ```json
   {
    "recommendations": [
        {
            "product_id": 315149,
            "product_name": "Ajar Hukum Pidana - Masruchin Rubai",
            "seller_id": 1409,
            "product_rating": 5,
            "product_price": 58900
        }
    ]
  }
  ```
