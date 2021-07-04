#!/bin/bash
while true
do
	git add .
	git commit -m "Routine push for webscraping"
	git push
	sleep 1800
done
