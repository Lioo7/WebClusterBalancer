FROM python:3.9.18

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# define a volume for storing logs
VOLUME /app/logs

CMD [ "python", "app.py" ]
