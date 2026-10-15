# v2 ideas (parking lot)

Ideas that are out of scope for v1 (public 25 Oct 2026). Nothing here is a commitment.

## Fillers

- **Ambiguous filler words ("so", "well", "right", "like").** Not counted in v1.
  They are also ordinary words ("turn right", "so much"), and a plain word
  match can't tell the two uses apart. On my own clips, 14 of 16 hits were
  "so", and I couldn't label them consistently by hand.
- **Sentence-initial "so".** A rule that can be applied the same way every
  time: count "so" only when it starts a sentence. It depends on Whisper's
  punctuation, which is a model prediction and not a measurement.
- **Detecting um/uh directly.** Whisper tends to drop them, so counting
  words from its text undercounts. A disfluency detector trained on audio is
  the main v2 project.
- **Self-corrections.** On clip 08 I said "actually", corrected myself to
  "really", and Whisper kept "actually" and dropped "really". Whisper's text
  hides the false start, so word counting can't see self-corrections. An
  audio-based disfluency detector could.

## Pauses

- **Pause tiers** (micro, hesitation, deliberate). Micro-pauses are below the
  resolution of Whisper's word timestamps, so this needs a better source of
  timing than Whisper's word times.
- **Audio-based leading-gap onset.** Use an energy threshold on the audio
  instead of Whisper's first-word start. Whisper reports 0.00 s when the real
  lead is under about 1 s.

## WER

- **Number normalization.** v1 doesn't normalize numbers, so "twenty-five"
  vs "25" and "nine" vs "9" each count as an error, though Whisper heard them
  right. Same for contractions ("do not" vs "don't") and spelling ("grey" vs
  "gray"). Rules for these would separate formatting from recognition errors.
- **Em dash and other non-ASCII punctuation.** `normalize()` strips
  `string.punctuation` only, which doesn't include "—". Not an issue for the
  current reference texts, which contain none.
