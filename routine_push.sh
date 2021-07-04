#!/bin/bash

while true
do
	git pull
	git add .
	git commit -m $(date +%s)
	git push
	sleep 1800
done
