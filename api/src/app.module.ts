import { Module } from '@nestjs/common';
import { AppController } from './app.controller.js';
import { SnippetsController } from './snippets/snippets.controller.js';
import { SnippetsService } from './snippets/snippets.service.js';

@Module({
  imports: [],
  controllers: [AppController, SnippetsController],
  providers: [SnippetsService],
})
export class AppModule {}
