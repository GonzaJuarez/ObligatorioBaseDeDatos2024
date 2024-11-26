FROM python:3.13

WORKDIR /app

COPY . .
RUN python -m venv env && . env/bin/activate
RUN pip install -r requirements.txt

CMD ["uvicorn", "API.app:app", "--host", "0.0.0.0", "--port", "8000"]