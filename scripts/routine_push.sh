#!/bin/bash

git pull
git add .
git commit -m $(date +%s)
git push
