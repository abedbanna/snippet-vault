import { BadRequestException, Injectable } from '@nestjs/common';
import { randomUUID } from 'node:crypto';
import { CreateSnippetInput, Snippet } from './snippet.js';

/** Returns the trimmed value, or throws a 400 naming the field if it is missing, blank, or longer than `max`. */
function requireText(
  input: unknown,
  field: keyof CreateSnippetInput,
  max: number,
): string {
  const value = (input as Record<string, unknown> | null)?.[field];
  const trimmed = typeof value === 'string' ? value.trim() : '';
  if (trimmed === '') {
    throw new BadRequestException(`${field} must not be blank`);
  }
  if (typeof value === 'string' && value.length > max) {
    throw new BadRequestException(`${field} must be at most ${max} characters`);
  }
  return trimmed;
}

@Injectable()
export class SnippetsService {
  private readonly snippets: Snippet[] = [];

  create(input: CreateSnippetInput): Snippet {
    const title = requireText(input, 'title', 200);
    const language = requireText(input, 'language', 40);
    requireText(input, 'code', 20000);
    const snippet: Snippet = {
      id: randomUUID(),
      title,
      language,
      code: input.code, // stored verbatim per the spec
      createdAt: new Date().toISOString(),
    };
    this.snippets.push(snippet);
    return snippet;
  }

  findAll(): Snippet[] {
    // Newest first: insertion order is creation order, so reverse a copy.
    return [...this.snippets];
  }

  /** Returns true if a snippet was removed, false if the id is unknown. */
  remove(id: string): boolean {
    const index = this.snippets.findIndex((s) => s.id === id);
    if (index === -1) return false;
    this.snippets.splice(index, 1);
    return true;
  }
}
