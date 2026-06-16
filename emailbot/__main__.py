"""Allow running the package with `python -m emailbot`."""

from emailbot.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
