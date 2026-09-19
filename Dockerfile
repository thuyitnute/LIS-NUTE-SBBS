FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Chạy server từ thư mục smart_boxes
CMD ["uvicorn", "smart_boxes.main:app", "--host", "0.0.0.0", "--port", "8000"]