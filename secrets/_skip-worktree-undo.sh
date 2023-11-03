#!/bin/sh

echo ":: Adding files from this directory back to the worktree."

git update-index --no-skip-worktree vpn/*/*.ovpn
git update-index --no-skip-worktree wap/*
git update-index --no-skip-worktree scorebot/*
git update-index --no-skip-worktree ../challenges/0_Smart-Home/_firmware/wap/config.h
git update-index --no-skip-worktree ../challenges/2_Power-Grid/_firmware/wap/config.h
git update-index --no-skip-worktree ../software/scorebot/secrets.py
git update-index --no-skip-worktree ../challenges/0_Smart-Home/t0/scorebot/secrets.py
