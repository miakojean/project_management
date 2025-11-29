# Dockerfile.vue (version développement uniquement)
FROM node:20-alpine

WORKDIR /project-management
COPY frontend/package*.json ./ 
RUN npm install

COPY project-management .

EXPOSE 5173
CMD ["npm", "run", "dev"]