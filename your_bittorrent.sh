#!/bin/sh

source .venv/bin/activate

exec python -m app.main "$@"