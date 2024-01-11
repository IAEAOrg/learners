# Base image
FROM klakegg/hugo:0.111.3-ext-ubuntu

# Set the working directory in the container
WORKDIR /src

# Install python and python-pip
RUN apt update && apt install -y python3-pip python3 python3-click python3-yaml wget unzip

# Copy the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]