#!/bin/bash

>test_compiler_output.txt

for folder in T{1..10}; do
  echo "============== $folder Started ==============="
  cp PA3_Resources/$folder/input.txt .
  python compiler.py
  ./tester_Linux.out >tester_output.txt
  diff PA3_Resources/$folder/expected.txt tester_output.txt -s >>test_compiler_output.txt
  echo "============== $folder Finished ==============="
done
