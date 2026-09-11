# Stage 1: install all deps, compile TypeScript, then drop dev deps
FROM node:22-alpine AS build
WORKDIR /app
# node:22 ships npm 10, which rejects this lock file (a transitive dev dep's
# typescript@5 peer). npm 11 matches the version the lock was generated with.
RUN npm install -g npm@11
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build && npm prune --omit=dev

# Stage 2: production deps + compiled output only
FROM node:22-alpine
WORKDIR /app
ENV NODE_ENV=production
COPY --from=build /app/package.json ./
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
USER node
EXPOSE 3000
CMD ["node", "dist/main"]
