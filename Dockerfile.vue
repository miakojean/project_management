# Dockerfile.vue → meant to be at repo root; docker-compose builds with context ./project-management
FROM node:20-bullseye-slim

# Use /app as the working directory to match docker-compose mounts
WORKDIR /app

# Copy only package files first for better caching (context is the frontend folder)
COPY package*.json ./
# Use npm install because there's no package-lock.json in the repo
RUN npm install --silent

# Some Rollup builds use optional native packages; ensure a compatible binary is present
# Install the GNU variant (Debian-based image) explicitly and rebuild native modules
RUN npm install @rollup/rollup-linux-x64-gnu --no-save || true
RUN npm rebuild --silent || true

# Copy the rest of the frontend source from the build context
COPY . ./

EXPOSE 5173

# Vite needs to listen on all interfaces when running inside Docker
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]