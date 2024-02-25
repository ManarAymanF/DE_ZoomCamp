FROM python:3.12

WORKDIR /app

# Install required dependencies
RUN apt-get update \
    && apt-get install -y wget libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only the necessary files
COPY import_data.py .

# Install Python packages
RUN pip install pandas sqlalchemy psycopg2 pyarrow

ENTRYPOINT [ "python", "import_data.py" ]
