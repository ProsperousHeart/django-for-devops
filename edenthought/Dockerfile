FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONBUFFERED=1
    # PIP_NO_CACHE_DIR=1 \
    # PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "edenthought.wsgi:application", "--workers=3"]