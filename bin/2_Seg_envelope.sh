#!/bin/bash

# Usage: ./2_Seg_envelope.sh Nidovirales.fasta 12 1.9 2.1 ../results/
# Output in ../results/

input_file="$1"
window_size="$2"
low_entropy_cutoff="$3"
high_entropy_cutoff="$4"
output_dir="$5"

file_name="$(basename $input_file | sed -r 's/^(.{2})/2_/g')"

high_complexity="${output_dir}/${file_name}_hi_complexity.faa"
low_complexity="${output_dir}/${file_name}_lo_complexity.faa"
combined_complexity="${output_dir}/${file_name}_complexity.faa"

seg "$input_file" -h "$window_size" "$low_entropy_cutoff" "$high_entropy_cutoff" > "$high_complexity"
seg "$input_file" -l "$window_size" "$low_entropy_cutoff" "$high_entropy_cutoff" > "$low_complexity"

cat "$high_complexity" > "$combined_complexity"
cat "$low_complexity" >> "$combined_complexity"

