FROM python:3.10-slim
WORKDIR /app
# Включаем UTF-8 на уровне всей операционной системы контейнера
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]