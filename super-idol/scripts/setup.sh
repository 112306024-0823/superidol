#!/bin/bash

# 設置後端
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt

# 設置前端
cd ../frontend
npm install 