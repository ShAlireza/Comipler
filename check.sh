#!/bin/bash

for i in {1..10}; do
  echo "Testing testcase T$i"
  cat PA2_Resources/T$i/input.txt >input.txt
  python compiler.py
  diff -isqw parse_tree.txt PA2_Resources/T$i/parse_tree.txt
  diff -isqw syntax_errors.txt PA2_Resources/T$i/syntax_errors.txt
  echo "=================================="
done
