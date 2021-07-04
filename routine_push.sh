#!/bin/bash

while true
do
	git add .
	git commit -m $(date +%s)
	git push
done
