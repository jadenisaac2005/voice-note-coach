def format_report(name, metrics, duration, n_words) -> str:
    if metrics is None:
        raise ValueError("metrics cannot be None")
    if metrics["pause_count"] == 0:
        run_on = f"No pause over 1 s: the whole clip was one stretch ({metrics['longest_run']['seconds']:.1f} s, {metrics['longest_run']['n_words']} words)"
    else:
        run_on = f"{metrics['longest_run']['seconds']:.1f} s, {metrics['longest_run']['n_words']} words"
    return f"""Voice-Note Coach: {name}
Duration (to last word): {duration:.1f} s     Words: {n_words}
Pace
  Speaking rate:      {metrics['speaking_rate']:.1f} WPM   (silence included)
  Articulation rate:  {metrics['articulation_rate']:.1f} WPM   (all gaps removed)
Pauses
  Count: {metrics['pause_count']}        (gap > 1 s)
  Time between words: {metrics['pause_ratio']*100:.1f} %  (all gaps, short ones included)
Fillers (um/uh only)
  Count: {metrics['fillers']}
Longest run-on (no pause > 1 s)
  {run_on}
Limits: Whisper often drops um/uh, so the filler count is a lower bound.
"""
