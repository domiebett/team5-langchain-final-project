FROM python:3.11-slim

COPY requirements.txt app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--logger.level=debug"]