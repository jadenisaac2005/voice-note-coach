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

## Pauses

- **Pause tiers** (micro, hesitation, deliberate). Micro-pauses are below the
  resolution of Whisper's word timestamps, so this needs a better source of
  timing than Whisper's word times.
