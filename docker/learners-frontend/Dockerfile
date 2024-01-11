# Base image
FROM node:19 as build-stage

# Set the working directory in the container
WORKDIR /app

# Install Git
RUN apt-get update && apt-get install -y git

# Repo info
ARG LEARNERS_GITHUB_REPO
ENV LEARNERS_GITHUB_REPO=${LEARNERS_GITHUB_REPO:-https://github.com/iaeaorg/learners}
ARG LEARNERS_GITHUB_BRANCH
ENV LEARNERS_GITHUB_BRANCH=${LEARNERS_GITHUB_BRANCH:-main-application}

# Set backend
ARG LEARNERS_BASE_URL
ENV LEARNERS_BASE_URL="${LEARNERS_BASE_URL:-}"
ENV VITE_BASEURL="${LEARNERS_BASE_URL:-}"
ENV VITE_BACKEND="${LEARNERS_BASE_URL:-}/api"

# Clone repo
RUN git clone --branch $LEARNERS_GITHUB_BRANCH $LEARNERS_GITHUB_REPO .

WORKDIR /app/frontend

# Install dependencies with Yarn
RUN yarn install

# Build the Vue app with Vite
RUN yarn build

# Use Nginx as the web server for serving the built Vue app
FROM nginx:stable-alpine as production-stage

# Copy the built app from previous stage
COPY --from=build-stage /app/frontend/dist /usr/share/nginx/html
RUN chmod 755 /usr/share/nginx/html

# Copy the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 443

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
