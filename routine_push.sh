#!/bin/bash
timestamp(){
	date + "%T"
}

while true
do
	git add .
	git commit -m timestamp
	git push
	sleep 1800
done
