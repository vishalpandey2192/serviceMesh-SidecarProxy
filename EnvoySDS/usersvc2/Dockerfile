# Base our image on the latest Envoy image.
FROM lyft/envoy:latest

# We need curl, pip, and dnsutils (for nslookup).
RUN apt-get update && apt-get -q install -y \
    curl \
    python-pip \
    dnsutils

# Set WORKDIR to /application which is the root of all our apps then COPY 
# only requirements.txt to avoid screwing up Docker caching and causing a
# full reinstall of all dependencies when dependencies are not changed.

WORKDIR /application
COPY requirements.txt .

# Install application dependencies
RUN pip install -r requirements.txt

# COPY the app code and configuration into place, then perform any final
# configuration steps.
COPY service.py .
COPY envoy.json .

# COPY the entrypoint script and make it runnable.
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]
