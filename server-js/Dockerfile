FROM node:20-slim
WORKDIR /app
RUN apt-get update && apt-get install -y git
COPY package.json ./
RUN npm install --omit=dev
COPY . .
EXPOSE 3000
CMD ["node", "bootstrap.js"]
