# build stage
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./
# install project dependencies
RUN npm install
COPY . .

# build app for production with minification
#RUN npm run build

EXPOSE 8080