#!/bin/bash

find . \( -type d -name .git -prune \) -o -type f -name "*.rst" -print0 | xargs -0 sed -i 's/\“/\"/g'

find . \( -type d -name .git -prune \) -o -type f -name "*.rst" -print0 | xargs -0 sed -i 's/\”/\"/g'

