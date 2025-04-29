#!/bin/bash

# 運行後端測試
cd backend
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
python -m pytest

# 運行前端測試
cd ../frontend
npm test 