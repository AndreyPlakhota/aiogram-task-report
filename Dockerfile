FROM python:3.9.2

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/


COPY . /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

#Установка порта
EXPOSE 8080
#установка часового пояса
ENV TZ Europe/Moscow

CMD ["python", "app.py"]