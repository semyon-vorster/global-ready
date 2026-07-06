FROM python:3.10-slim
WORKDIR /app
COPY . .
# Вот эта строчка вылечит ошибку кодировки раз и навсегда:
ENV PYTHONIOENCODING=utf-8
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]