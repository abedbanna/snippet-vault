import { Body, Controller, Get, Post } from '@nestjs/common';
import type { CreateSnippetInput, Snippet } from './snippet.js';
import { SnippetsService } from './snippets.service.js';

@Controller('snippets')
export class SnippetsController {
  constructor(private readonly snippets: SnippetsService) {}

  @Post()
  create(@Body() body: CreateSnippetInput): Snippet {
    return this.snippets.create(body);
  }

  @Get()
  findAll(): Snippet[] {
    return this.snippets.findAll();
  }
}
