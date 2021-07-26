FROM python:3.7

COPY . /app
RUN pip install -r app/requirements.txt
EXPOSE 8501

CMD ["streamlit", "run", "app/app.py"]