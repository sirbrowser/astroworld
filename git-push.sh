#!/usr/bin/sh
echo Benjamin pd
echo Commit message?
read message
git add .
git commit -m "$message"
git push
git push --tags
