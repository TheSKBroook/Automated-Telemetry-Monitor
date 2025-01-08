FROM python:3.9-slim

WORKDIR /app

COPY feature/. /app/

COPY inventory.ini /app/
# Install the dependencies

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir ansible && \
    pip install --no-cache-dir -r requirements.txt


#  Expose the required ports
EXPOSE 5100 5200

CMD ["sh", "-c", "python3 webhook/webhook.py > webhook.log 2>&1 & python3 line/line.py > line.log 2>&1 & wait"]

# CMD ["sh", "-c", "python3 line/line.py > line.log 2>&1 & wait"]

# CMD ["sh", "-c", "python3 webhook/webhook.py > webhook.log 2>&1 wait"]

# CMD ["sh", "-c", "python3 control.py & python3 line/line.py & wait"]
