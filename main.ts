// Entry point for the news-image-20261126 V2 submission.
// The deliverable is the poster rendered by render.py (entry.png).
// This program checks that the poster exists, is a real PNG of the
// expected dimensions, and copies it to the output directory the
// grader reads. Run render.py first, then:  node main.ts

import { copyFileSync, existsSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = fileURLToPath(new URL('.', import.meta.url));
const poster = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

if (!existsSync(poster)) {
  throw new Error('entry.png is missing — run `python3 render.py` first');
}

const bytes = readFileSync(poster);
const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
const isPng = PNG_SIGNATURE.every((b, i) => bytes[i] === b);
if (!isPng) {
  throw new Error('entry.png does not carry a PNG signature');
}

// IHDR width/height sit at bytes 16..24, big-endian.
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== 1024 || height !== 1004) {
  throw new Error(`unexpected poster size ${width}x${height}, expected 1024x1004`);
}

copyFileSync(poster, join(outDir, 'entry.png'));
console.log(
  `entry.png verified (${width}x${height}, ${statSync(poster).size} bytes) and copied to ${outDir}`,
);
