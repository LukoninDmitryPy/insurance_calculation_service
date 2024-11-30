FROM python:3.10

WORKDIR /app

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

COPY ./src /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
