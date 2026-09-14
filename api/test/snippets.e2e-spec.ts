import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication } from '@nestjs/common';
import request from 'supertest';
import { App } from 'supertest/types';
import { AppModule } from './../src/app.module.js';

describe('Snippets (e2e)', () => {
  let app: INestApplication<App>;

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

  it('GET /snippets on an empty vault returns []', () => {
    return request(app.getHttpServer()).get('/snippets').expect(200).expect([]);
  });

  it('POST /snippets then GET /snippets lists it, newest first', async () => {
    const first = { title: 'First', language: 'ts', code: 'const a = 1;' };
    const second = { title: 'Second', language: 'js', code: 'var b = 2;' };

    const created = await request(app.getHttpServer())
      .post('/snippets')
      .send(first)
      .expect(201);
    expect(created.body).toMatchObject(first);
    expect(typeof created.body.id).toBe('string');
    expect(typeof created.body.createdAt).toBe('string');

    await request(app.getHttpServer())
      .post('/snippets')
      .send(second)
      .expect(201);

    const list = await request(app.getHttpServer())
      .get('/snippets')
      .expect(200);
    expect(list.body).toHaveLength(2);
    expect(list.body[0]).toMatchObject(second);
    expect(list.body[1]).toEqual(created.body);
  });
});
