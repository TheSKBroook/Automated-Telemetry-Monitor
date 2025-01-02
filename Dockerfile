FROM python:3.9-slim

WORKDIR /app

COPY feature/ /app/

# Copy requirements.txt into the container
COPY deploy/requirements.txt /app/

COPY inventory.ini /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the required ports
EXPOSE 5000 5100

CMD ["sh", "-c", "python3 control.py & python3 line/line.py & wait"]
