# Ubuntu 18.04 base with Python runtime and pyodbc to connect to SQL Server
FROM ubuntu:18.04

# apt-get and system utilities
RUN apt-get update && apt-get install -y \
    curl apt-utils apt-transport-https debconf-utils gcc build-essential g++-5\
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
 && apt-get install unixodbc -y \
 && apt-get install unixodbc-dev -y \
 && apt-get install tdsodbc -y \
 && apt-get install --reinstall build-essential -y

RUN curl --fail https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl --fail https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools

# python libraries
RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

# install necessary locales, this prevents any locale errors related to Microsoft packages
RUN apt-get update && apt-get install -y locales \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
WORKDIR /app
COPY . .
EXPOSE 5000 
CMD ["python3","-u","service.py"]