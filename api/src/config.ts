// Runtime configuration read from environment variables.
// See .env.example for the supported keys.

const DEFAULT_PORT = 3000;
const DEFAULT_CORS_ORIGIN = 'http://localhost:5173';

function readPort(): number {
  const raw = process.env.PORT;
  if (raw === undefined || raw === '') return DEFAULT_PORT;
  const port = Number(raw);
  if (!Number.isInteger(port) || port < 1 || port > 65535) {
    throw new Error(
      `Invalid PORT "${raw}": expected an integer between 1 and 65535`,
    );
  }
  return port;
}

function readCorsOrigin(): string {
  const raw = process.env.CORS_ORIGIN?.trim();
  if (!raw) return DEFAULT_CORS_ORIGIN;
  if (raw === '*') {
    throw new Error('CORS_ORIGIN must be a specific origin, not "*"');
  }
  return raw;
}

export const config = {
  port: readPort(),
  corsOrigin: readCorsOrigin(),
} as const;
