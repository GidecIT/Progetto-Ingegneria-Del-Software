FROM node:20-alpine

WORKDIR /usr/src/app

COPY src/frontend/package.json src/frontend/package-lock.json ./
RUN npm install

COPY src/frontend/ ./

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
