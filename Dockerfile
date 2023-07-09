FROM python:3.10-slim
## Docker Config
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /home/app
COPY . .
EXPOSE 8000
RUN chmod +x ./run.sh

CMD ./run.sh