#!/bin/bash

function call {
	echo "calling"
	curl -X GET "http://localhost:5000/active_cases?limit=10" -H  "accept: application/json" >> test.log
}

for i in `seq 1 20`
do 
	call &

done
