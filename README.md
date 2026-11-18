# The World in One Day — 18 November 2026

A program that generates a single summary image of the most important world
news first published on 18 November 2026 (UTC).

## How it works

`python3 generate.py` (or `./run.sh`) renders `output.png` (1600 x 900 PNG)
using only generated shapes, lines, fills, gradients and text — no photos,
no copied artwork, no logos.

`main.py` is the same generator, provided as the entry point for the
submission checks.

## Stories

Five stories, each from at least two reputable sources, ranked by importance
for a global audience:

1. APEC opens in Shenzhen as Xi urges free and open trade
2. Bahrain and Kuwait intercept Iranian air attacks
3. Trump holds state visit with Marcos in Manila
4. Voyager 1 reaches one light-day from Earth
5. Bezos says he helped pick Pattinson as Bond

## Files

- `output.png` — the summary image (1600 x 900)
- `generate.py` / `main.py` — the image generator
- `run.sh` — reproduces `output.png` from scratch, no network, no API keys
- `sources.md` — sources for every story, plus the stories excluded and why
- `transcript.md` — transcript of the AI conversations that wrote the code

## Reproduce

```bash
./run.sh
```

Regenerates `output.png` in under a second, with an identical result.
