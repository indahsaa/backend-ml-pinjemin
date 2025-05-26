from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import numpy as np
import tensorflow as tf
import joblib
from scipy.sparse import load_npz
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os

app = FastAPI()


model_user = tf.keras.models.load_model("models/model.h5", compile=False)
model_search = tf.keras.models.load_model("models/model_final.h5", compile=False)
model_item = tf.keras.models.load_model("models/recommendation_model.h5", compile=False)


vectorizer = joblib.load("models/vectorizer.pkl")
tfidf_matrix = load_npz("models/tfidf_matrix.npz")

df = pd.read_csv("models/all_dataset.csv")
df = df.reset_index(drop=True)  
product_data = {}
product_id_to_index = {}
index_to_product_id = {}

def safe_float(val, default=0.0):
    try:
        return float(val)
    except (ValueError, TypeError):
        return default

for idx, row in df.iterrows():
    product_id = int(row["product_id"])
    product_data[idx] = {
        "product_name": row["product_name"],
        "seller_id": int(row["seller_id"]),
        "product_rating": safe_float(row.get("product_rating")),
        "product_price": safe_float(row.get("product_price")),
        
    }
    product_id_to_index[product_id] = idx
    index_to_product_id[idx] = product_id

NUM_CATEGORIES = 10  



class RecommendationRequest(BaseModel):
    user_id: int
    top_n: int = 10

class SearchRequest(BaseModel):
    keyword: str
    top_n: int = 10

class ProductRecommendation(BaseModel):
    product_id: int
    product_name: str = None
    seller_id: int = None
    product_rating: float = None
    product_price: float = None

class RecommendationResponse(BaseModel):
    recommendations: List[ProductRecommendation]

def build_recommendations(scores: np.ndarray, top_n: int) -> List[ProductRecommendation]:
   
    top_indices = scores.argsort()[-top_n:][::-1]
    recs = []
    for idx in top_indices:
        info = product_data.get(idx, {})
        recs.append(ProductRecommendation(
            product_id=index_to_product_id.get(idx, idx),
            product_name=info.get("product_name"),
            seller_id=info.get("seller_id"),
            product_rating=info.get("product_rating"),
            product_price=info.get("product_price"),
        ))
    return recs

# Endpoint user-based recommendation
@app.post("/recommend/user", response_model=RecommendationResponse)
def recommend_user(req: RecommendationRequest):
    
    user_vector = np.array([[req.user_id]])
    scores = model_user.predict(user_vector, verbose=0)[0]
    recommendations = build_recommendations(scores, req.top_n)
    return RecommendationResponse(recommendations=recommendations)

# Endpoint search-based recommendation
@app.post("/recommend/search", response_model=RecommendationResponse)
def recommend_search(req: SearchRequest):
  
    query_vec = vectorizer.transform([req.keyword.lower()])
    cosine_sim = cosine_similarity(query_vec, tfidf_matrix).flatten()

   
    candidate_indices = cosine_sim.argsort()[-50:][::-1]
    hasil = []

    for idx in candidate_indices:
        if idx not in product_data:
            continue
        produk_tfidf_vec = tfidf_matrix[idx].toarray().flatten()
      
        if "category_label" in df.columns:
            category_label = df.iloc[idx].get("category_label", None)
            if category_label is not None and not pd.isna(category_label):
                category_label = int(category_label)
                category_one_hot = np.zeros(NUM_CATEGORIES)
                if 0 <= category_label < NUM_CATEGORIES:
                    category_one_hot[category_label] = 1
                else:
                    category_one_hot = np.zeros(NUM_CATEGORIES)
            else:
                category_one_hot = np.zeros(NUM_CATEGORIES)
        else:
            category_one_hot = np.zeros(NUM_CATEGORIES)
      
        expected_input_dim = model_search.input_shape[-1]
        tfidf_len = expected_input_dim - NUM_CATEGORIES
        produk_tfidf_vec = produk_tfidf_vec[:tfidf_len]
        x_input = np.concatenate([category_one_hot, produk_tfidf_vec]).reshape(1, -1)
        prob = model_search.predict(x_input, verbose=0)[0][0]
        hasil.append((prob, idx))

    hasil_sorted = sorted(hasil, key=lambda x: x[0], reverse=True)[:req.top_n]
    recommendations = []
    for score, idx in hasil_sorted:
        info = product_data.get(idx, {})
        recommendations.append(ProductRecommendation(
            product_id=index_to_product_id.get(idx, idx),
            score=float(score),
            product_name=info.get("product_name"),
            seller_id=info.get("seller_id"),
            product_rating=info.get("product_rating"),
            product_price=info.get("product_price"),
        ))
    return RecommendationResponse(recommendations=recommendations)


class ItemRequest(BaseModel):
    product_id: int
    top_n: int = 10


@app.post("/recommend/item", response_model=RecommendationResponse)
def recommend_item(req: ItemRequest):
    if req.product_id not in product_id_to_index:
        return RecommendationResponse(recommendations=[])
    query_index = product_id_to_index[req.product_id]

    
    X_all = tfidf_matrix.toarray()
    if X_all.shape[1] > model_item.input_shape[-1]:
        X_all = X_all[:, :model_item.input_shape[-1]]
    elif X_all.shape[1] < model_item.input_shape[-1]:
        pad_width = model_item.input_shape[-1] - X_all.shape[1]
        X_all = np.pad(X_all, ((0,0),(0,pad_width)), mode='constant')

   
    item_embeddings = model_item.predict(X_all, verbose=0)

    if len(item_embeddings.shape) == 2:
        query_embedding = item_embeddings[query_index].reshape(1, -1)
        similarities = cosine_similarity(query_embedding, item_embeddings)[0]
    
    else:
        similarities = item_embeddings.flatten()
        similarities[query_index] = -np.inf  

    similar_indices = similarities.argsort()[::-1]
    similar_indices = [i for i in similar_indices if i != query_index][:req.top_n]
    recommendations = []
    for idx in similar_indices:
        pid = index_to_product_id.get(idx, None)
        info = product_data.get(idx, {})
        if not info and pid is not None:
            idx2 = product_id_to_index.get(pid)
            info = product_data.get(idx2, {})
        recommendations.append(ProductRecommendation(
            product_id=pid if pid is not None else idx,
            score=float(similarities[idx]),
            product_name=info.get("product_name"),
            seller_id=info.get("seller_id"),
            product_rating=info.get("product_rating"),
            product_price=info.get("product_price"),
        ))
    return RecommendationResponse(recommendations=recommendations)
