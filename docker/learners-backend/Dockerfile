# Base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install Git
RUN apt-get update && apt-get install -y python3-pip

# Repo info
ARG LEARNERS_GITHUB_REPO
ENV LEARNERS_GITHUB_REPO=${LEARNERS_GITHUB_REPO:-https://github.com/ait-cs-IaaS/learners}
ARG LEARNERS_GITHUB_BRANCH
ENV LEARNERS_GITHUB_BRANCH=${LEARNERS_GITHUB_BRANCH:-feature/drawio_integration}

# Install backend via git
RUN pip3 install $LEARNERS_GITHUB_REPO/archive/refs/heads/$LEARNERS_GITHUB_BRANCH.zip

# Expose port
EXPOSE 5000

# Copy the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]