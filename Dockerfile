FROM python:3.10-alpine
WORKDIR app/
COPY . .
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
CMD ["sh", "-c", "python3 main.py & uvicorn web.app:app --host 0.0.0.0 --port 8001"]
