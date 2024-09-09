FROM python:3.10.5-slim
ENV PYTHONPATH=/api
WORKDIR /api
COPY ./requirements.txt /api/requirements.txt

RUN pip install -r requirements.txt

COPY . /api

## program run methods
CMD ["uvicorn", "app.main:app", "--host" , "0.0.0.0" , "--port" , "8000" , "--reload"]
