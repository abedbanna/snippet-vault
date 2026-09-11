import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication } from '@nestjs/common';
import request from 'supertest';
import { App } from 'supertest/types';
import { AppModule } from './../src/app.module.js';

const UUID_V4 =
  /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

describe('Snippets (e2e)', () => {
  let app: INestApplication<App>;

  const validSnippet = {
    title: 'Debounce',
    language: 'typescript',
    code: 'export const debounce = () => {};',
  };

  beforeEach(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();
  });

  afterEach(async () => {
    await app.close();
  });

  describe('S1. Save a snippet', () => {
    it('POST /snippets with valid fields returns 201 with the created snippet', async () => {
      const res = await request(app.getHttpServer())
        .post('/snippets')
        .send(validSnippet)
        .expect(201);

      expect(res.body).toMatchObject(validSnippet);
      expect(res.body.id).toMatch(UUID_V4);
      expect(new Date(res.body.createdAt).toISOString()).toBe(
        res.body.createdAt,
      );
    });

    it.each([
      ['title', ''],
      ['title', '   '],
      ['language', ''],
      ['language', '   '],
      ['code', ''],
      ['code', '   '],
    ])(
      'POST /snippets returns 400 and saves nothing when %s is %j',
      async (field, value) => {
        await request(app.getHttpServer())
          .post('/snippets')
          .send({ ...validSnippet, [field]: value })
          .expect(400);

        await request(app.getHttpServer())
          .get('/snippets')
          .expect(200)
          .expect([]);
      },
    );

    it.each([
      ['title', 200],
      ['language', 40],
      ['code', 20000],
    ])(
      'POST /snippets returns 400 naming the field and limit when %s exceeds %i characters',
      async (field, limit) => {
        const res = await request(app.getHttpServer())
          .post('/snippets')
          .send({ ...validSnippet, [field]: 'x'.repeat(limit + 1) })
          .expect(400);

        expect(res.body.message).toBe(
          `${field} must be at most ${limit} characters`,
        );
      },
    );
  });

  describe('S2. See my snippets', () => {
    it('GET /snippets on an empty vault returns []', () => {
      return request(app.getHttpServer())
        .get('/snippets')
        .expect(200)
        .expect([]);
    });

    it('GET /snippets returns all saved snippets newest first', async () => {
      const first = { title: 'First', language: 'ts', code: 'const a = 1;' };
      const second = { title: 'Second', language: 'js', code: 'var b = 2;' };
      const third = { title: 'Third', language: 'py', code: 'c = 3' };

      const created = [];
      for (const body of [first, second, third]) {
        const res = await request(app.getHttpServer())
          .post('/snippets')
          .send(body)
          .expect(201);
        created.push(res.body);
      }

      const list = await request(app.getHttpServer())
        .get('/snippets')
        .expect(200);

      expect(list.body).toEqual([created[2], created[1], created[0]]);
    });
  });

  describe('S4. Delete a snippet', () => {
    it('DELETE /snippets/:id returns 204 and removes the snippet from the list', async () => {
      const keep = await request(app.getHttpServer())
        .post('/snippets')
        .send({ title: 'Keep', language: 'ts', code: 'keep()' })
        .expect(201);
      const gone = await request(app.getHttpServer())
        .post('/snippets')
        .send({ title: 'Gone', language: 'ts', code: 'gone()' })
        .expect(201);

      await request(app.getHttpServer())
        .delete(`/snippets/${gone.body.id}`)
        .expect(204)
        .expect('');

      await request(app.getHttpServer())
        .get('/snippets')
        .expect(200)
        .expect([keep.body]);
    });

    it('DELETE /snippets/:id returns 404 for an unknown id', () => {
      return request(app.getHttpServer())
        .delete('/snippets/does-not-exist')
        .expect(404);
    });
  });
});
