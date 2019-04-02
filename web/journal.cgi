#!/bin/bash
set -e -o pipefail

printf 'Content-Disposition: inline;filename=%s-journal-%s.tsv\n' "$(hostname -s)" "$(date +%Y-%m-%d)"
printf 'Content-Type: text/tab-separated-values\n'
printf '\n'

declare -A prefix=()
while IFS="=" read dir num; do
    if [[ -z ${dir} ]]; then continue; fi
    prefix[${dir}]="$num"
done < ${ETC:-/etc}/cart/playboxes

while read t h skip file; do
    skip="${skip#skip=}"
    file="${file#file=}"
    dir="${file%/*}"
    p="${prefix[$dir]}"
    file="${p}${file##*/}"
    printf '%s\t%s\t%s\t%s\n' "$t" "$h" "$skip" "$file"
done < <(sudo journalctl -oshort-iso --identifier=thevoice | grep ' play ' | cut -d' ' -f1,2,5-)
