#!/bin/bash

script_dir="$1"

yarrrml-parser -i "$script_dir/general.yarrrml" -o "$script_dir/general.rml.ttl"
