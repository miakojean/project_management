# Dockerfile.vue → à mettre à la racine du projet
FROM node:20-alpine

WORKDIR /project-management

COPY project-management/package*.json ./
RUN npm ci   # plus propre que npm install

COPY project-management/ .

EXPOSE 5173

# Très important : Vite doit écouter sur toutes les interfaces
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]