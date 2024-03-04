#!/bin/bash

script_dir="$1"

java -jar "$script_dir/rmlmapper-6.5.1-r371-all.jar" -s turtle -m "$script_dir/general.rml.ttl" -o "$script_dir/invoice.ttl"
