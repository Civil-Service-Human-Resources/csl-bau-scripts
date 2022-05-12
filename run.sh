#!/usr/bin/env bash

export PYTHONPATH=$(dirname "$0")
python $1 "${@:2}"