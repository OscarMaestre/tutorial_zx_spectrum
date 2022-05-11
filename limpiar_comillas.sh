#!/bin/bash

reemplazos=('s/\“/\"/g' 's/\”/\"/g' 's/\»/\>>/g' 's/\«/\<</g', 's/\…/\.../g')

for reemplazo in "${reemplazos[@]}"
do
    echo "$reemplazo"
    find . \( -type d -name .git -prune \) -o -type f -name "*.rst" -print0 | xargs -0 sed -i "$reemplazo"
done

