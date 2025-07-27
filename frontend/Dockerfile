FROM node:22-slim

WORKDIR /app

COPY . .

RUN npm install

EXPOSE 5173

CMD ["npm", "run", "dev"]

# Prod build is commented

# FROM node:22-alpine3.21

# WORKDIR /app
# COPY . .

# RUN npm ci
# RUN npm run build

# RUN npm install -g serve
# CMD ["serve", "-s", "dist", "-l", "5173"]
