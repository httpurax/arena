#!/usr/bin/env node
/**
 * verify-deck.js — mechanical pre-delivery check for populated flashcard decks.
 *
 * Usage:  node verify-deck.js <deck.html> [more.html ...]
 *
 * Checks each deck:
 *   1. STUDY DATA / END STUDY DATA markers are present
 *   2. STUDY_DATA parses as JavaScript
 *   3. Shape is { title, flashcards[], quiz[] } with the documented keys
 *   4. Flashcard ids are unique (they are spaced-repetition storage keys)
 *   5. Every quiz answer is valid for its type
 *        mc    -> exactly 4 options, answer is an index in range
 *        tf    -> answer is a boolean
 *        short -> answer is a non-empty string
 *   6. No raw "<" inside the data block (could close the <script> tag)
 *   7. No literal "</script>" or "<!--" inside the data block
 *   8. App logic below END STUDY DATA is byte-identical to the bundled template
 *
 * Exits 0 when every deck passes, 1 on any failure, 2 on a usage error.
 */
'use strict';

const fs = require('fs');
const path = require('path');

const MARK_START = 'const STUDY_DATA = ';
const MARK_END = '/* ==================== END STUDY DATA';

function extract(html) {
  const start = html.indexOf(MARK_START);
  const end = html.indexOf(MARK_END);
  if (start < 0 || end < 0) return { error: 'STUDY DATA markers not found' };
  return {
    block: html.slice(start, end).replace(/;\s*$/, ''),
    head: html.slice(0, start),
    tail: html.slice(end),
  };
}

function validate(deck) {
  const errs = [];
  if (!deck || typeof deck !== 'object') return ['STUDY_DATA is not an object'];
  if (typeof deck.title !== 'string' || !deck.title.trim()) errs.push('title is missing or empty');
  if (!Array.isArray(deck.flashcards)) errs.push('flashcards is not an array');
  if (!Array.isArray(deck.quiz)) errs.push('quiz is not an array');

  const cards = Array.isArray(deck.flashcards) ? deck.flashcards : [];
  const ids = cards.map((c) => c && c.id);
  if (new Set(ids).size !== ids.length) errs.push('flashcard ids are not unique');
  cards.forEach((c, i) => {
    if (!c || typeof c !== 'object') { errs.push(`flashcard ${i + 1} is not an object`); return; }
    ['id', 'front', 'back'].forEach((k) => {
      if (typeof c[k] !== 'string' || !c[k].trim()) errs.push(`flashcard ${i + 1} field "${k}" is missing or empty`);
    });
  });

  const quiz = Array.isArray(deck.quiz) ? deck.quiz : [];
  quiz.forEach((q, i) => {
    const n = i + 1;
    if (!q || typeof q !== 'object') { errs.push(`quiz ${n} is not an object`); return; }
    if (typeof q.question !== 'string' || !q.question.trim()) errs.push(`quiz ${n} question is missing`);
    if (!['mc', 'tf', 'short'].includes(q.type)) { errs.push(`quiz ${n} has unknown type "${q.type}"`); return; }
    if (q.type === 'mc') {
      if (!Array.isArray(q.options) || q.options.length !== 4) errs.push(`quiz ${n} must have exactly 4 options`);
      else if (!(Number.isInteger(q.answer) && q.answer >= 0 && q.answer < q.options.length)) errs.push(`quiz ${n} answer ${q.answer} is not a valid option index`);
    } else if (q.type === 'tf') {
      if (typeof q.answer !== 'boolean') errs.push(`quiz ${n} tf answer must be a boolean`);
    } else if (typeof q.answer !== 'string' || !q.answer.trim()) {
      errs.push(`quiz ${n} short answer must be non-empty text`);
    }
  });

  return errs;
}

function main() {
  const files = process.argv.slice(2);
  if (!files.length) {
    console.error('usage: node verify-deck.js <deck.html> [more.html ...]');
    process.exit(2);
  }

  const templatePath = path.join(__dirname, '..', 'assets', 'flashcard-quiz-app.html');
  const template = fs.existsSync(templatePath) ? fs.readFileSync(templatePath, 'utf8') : null;
  const templateParts = template ? extract(template) : null;

  let failed = 0;

  for (const file of files) {
    if (!fs.existsSync(file)) {
      console.error(`MISSING FILE: ${file}`);
      failed++;
      continue;
    }
    const html = fs.readFileSync(file, 'utf8');
    const parts = extract(html);
    if (parts.error) {
      console.error(`FAIL ${file} — ${parts.error}`);
      failed++;
      continue;
    }

    const problems = [];
    if (parts.block.includes('<')) problems.push('raw "<" inside the data block');
    if (parts.block.includes('</' + 'script')) problems.push('literal </script> inside the data block');
    if (parts.block.includes('<!--')) problems.push('literal <!-- inside the data block');

    let deck;
    try {
      deck = eval('(' + parts.block.replace(MARK_START, '') + ')');
    } catch (e) {
      console.error(`FAIL ${file} — STUDY_DATA does not parse: ${e.message}`);
      failed++;
      continue;
    }

    problems.push(...validate(deck));

    if (templateParts && !templateParts.error && parts.tail !== templateParts.tail) {
      problems.push('app logic below END STUDY DATA differs from the bundled template');
    }

    const cards = Array.isArray(deck.flashcards) ? deck.flashcards.length : 0;
    const quiz = Array.isArray(deck.quiz) ? deck.quiz.length : 0;
    if (problems.length) {
      failed++;
      console.error(`FAIL ${file} — ${cards} cards, ${quiz} quiz`);
      problems.forEach((p) => console.error(`   - ${p}`));
    } else {
      console.log(`PASS ${file} — ${cards} cards, ${quiz} quiz`);
    }
  }

  process.exit(failed ? 1 : 0);
}

main();
