FROM node:20-alpine

RUN apk add --no-cache bash curl netcat-openbsd

WORKDIR /app

COPY package*.json ./
RUN npm ci

# código
COPY tsconfig*.json ./
COPY src ./src
COPY ormconfig.ts ./

RUN npx tsc -p tsconfig.json

COPY docker/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 3000
CMD ["/app/entrypoint.sh"]
