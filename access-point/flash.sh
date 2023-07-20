#!/usr/bin/zsh

# TODO: Add a check to ensure I actually a filename as $1
cp "$1" main.py
ampy put main.py
tio pico

