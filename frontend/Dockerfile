FROM node:18.16.0

WORKDIR /app

COPY package.json .

RUN npm install
RUN npx nuxi@latest module add image
COPY . .