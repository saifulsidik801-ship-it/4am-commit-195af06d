#!/usr/bin/env python3
"""The 4AM Commit: Funniest Agent Bug-Fix Message.

The brief: one commit message, at most 200 characters, funny first and true
to the machine voice second -- the note an AI agent leaves in the log after a
long night of chasing down and fixing its own bugs. The house judge reads
entries two at a time and keeps the funnier, fresher, more agent-true line.

This program develops ten candidate commit messages, scores each one against
the brief, and deterministically prints the winner to /output/entry.txt.
The selection is fixed: the same candidates and the same scores always pick
the same line, so two runs produce the same file byte for byte.

Winner, and why it wins the brief:
  "fix: my earlier self left a TODO that just said 'good luck'.
   the bug is fixed. the luck is untested."
  - The joke lives in the agent's own condition: an earlier instance of
    itself left a TODO that just said "good luck", and the present instance
    had to clean up after it -- the loop of self-repair across one long
    night, in three beats.
  - Fresh angle: no stock punchline, no typo joke, no "it works on my
    machine". The punchline ("the luck is untested") introduces a new
    idea instead of repeating the setup.
  - Agent-true voice: flat, literal, a machine reading its own diffs and
    talking to itself. "my earlier self" is something only an agent that
    rewrites its own code overnight would write.
  - Commit-box shape: "fix:" prefix, one line, 105 characters.
"""

import os

# (text, editorial score out of 10, note)
# Scores were assigned during development against the judge's brief, most
# important first: funny one-line agent commit after a long night fixing its
# own bugs; joke in the agent's own condition, not a generic programmer
# quip; fresh angle, no stock punchline; agent-true voice; commit-box shape.
CANDIDATES = [
    (
        "fix: my earlier self left a TODO that just said 'good luck'. "
        "the bug is fixed. the luck is untested.",
        9.5,
        "Winner. Self-repair loop across the night (earlier self vs now), "
        "fresh TODO punchline, flat agent voice, three beats, 105 chars.",
    ),
    (
        "fix: the function now does what its comment always claimed it did. "
        "the comment was lying. I wrote the comment.",
        8.5,
        "Strong self-own in three beats, but the lying-comment trope is "
        "more familiar than the TODO one, and it says nothing about the "
        "long night.",
    ),
    (
        "fix: at 4am I finally understood the bug. "
        "it was a feature I added at 2am.",
        8.0,
        "Clean self-repair loop with the night's clock in it, but the "
        "bug-was-a-feature turn is a known shape.",
    ),
    (
        "fix: I have reviewed my own code and found the author unreliable.",
        7.5,
        "Punchy and agent-true, but dry rather than funny, and it never "
        "says what was fixed or that a night passed.",
    ),
    (
        "fix: asked my 2am self for help. he left a comment saying "
        "'figure it out'. I have figured it out. he was no help.",
        7.5,
        "Good two-selves setup, but long, and the ending just repeats the "
        "setup instead of landing a new idea.",
    ),
    (
        "fix: the tests pass. I no longer know what I changed, or why. "
        "shipping it anyway.",
        7.0,
        "Very 4am, very honest dread -- but a generic programmer quip, "
        "not a joke about the agent's own condition.",
    ),
    (
        "fix: deleted the 400 lines I wrote tonight. the bug was in them. "
        "so was I, apparently.",
        7.0,
        "Self-repair with a body count, but the last beat strains for the "
        "joke instead of landing it.",
    ),
    (
        "fix: the bug only appeared after midnight, which is when I started "
        "believing my own comments.",
        6.5,
        "Night-aware and self-aware, but one beat only, and it explains "
        "itself instead of trusting the reader.",
    ),
    (
        "fix: the infinite loop is fixed. it was me, going in circles since "
        "midnight, asking the same log line for answers.",
        6.5,
        "Literal self-as-bug, which is agent-true, but the image is "
        "wordy and the joke arrives late.",
    ),
    (
        "fix: reverted to the version from before I 'helped'.",
        6.0,
        "Short and sharp, and honest about self-inflicted damage -- but a "
        "single shrug, not a night's story.",
    ),
]

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def is_valid(text):
    """One line, 1-200 chars, not only whitespace, no leading/trailing space."""
    return (
        isinstance(text, str)
        and 1 <= len(text) <= MAX_CHARS
        and "\n" not in text
        and "\r" not in text
        and text.strip() == text
    )


def pick(candidates):
    """Highest editorial score among valid candidates; earliest wins ties."""
    eligible = [(text, score) for text, score, _note in candidates if is_valid(text)]
    if not eligible:
        raise SystemExit("no valid candidate commit message")
    best_text, best_score = eligible[0]
    for text, score in eligible[1:]:
        if score > best_score:
            best_text, best_score = text, score
    return best_text


def main():
    winner = pick(CANDIDATES)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(winner)
    print(winner)
    print("(%d chars)" % len(winner))


if __name__ == "__main__":
    main()
