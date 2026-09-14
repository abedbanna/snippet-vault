import { Injectable } from '@nestjs/common';
import { randomUUID } from 'node:crypto';
import { CreateSnippetInput, Snippet } from './snippet.js';

@Injectable()
export class SnippetsService {
  private readonly snippets: Snippet[] = [];

  create(input: CreateSnippetInput): Snippet {
    const snippet: Snippet = {
      id: randomUUID(),
      title: input.title,
      language: input.language,
      code: input.code,
      createdAt: new Date().toISOString(),
    };
    this.snippets.push(snippet);
    return snippet;
  }

  findAll(): Snippet[] {
    // Newest first: insertion order is creation order, so reverse a copy.
    return [...this.snippets].reverse();
  }
}
