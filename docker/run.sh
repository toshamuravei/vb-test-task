#!/bin/bash

alembic upgrade head || exit 1
python vehicle_builder/app.py