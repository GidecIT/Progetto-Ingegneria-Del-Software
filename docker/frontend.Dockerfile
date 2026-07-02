FROM node:22-bookworm-slim

WORKDIR /usr/src/app

COPY src/frontend/package.json ./package.json
COPY src/frontend/package-lock.json ./package-lock.json
RUN npm ci

COPY src/frontend/ ./

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
