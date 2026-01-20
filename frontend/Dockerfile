FROM node:24-alpine AS development

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

FROM node:24-alpine AS builder

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

RUN npm run build

FROM node:24-alpine AS production

WORKDIR /app

COPY --from=builder /app/build ./build
COPY --from=builder /app/package*.json ./

RUN npm ci --production

EXPOSE 3000

CMD ["node", "build"]
