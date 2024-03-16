FROM postgres:latest
ENV POSTGRES_USER=lab3_user
ENV POSTGRES_PASSWORD=lab3_password
ENV POSTGRES_DB=lab3_db
COPY init.sql /docker-entrypoint-initdb.d/
