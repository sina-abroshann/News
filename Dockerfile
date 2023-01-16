FROM python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /docker-data/news
COPY requirements.txt /docker-data/news
RUN pip install -r requirements.txt
EXPOSE 8000
COPY . /docker-data/news
