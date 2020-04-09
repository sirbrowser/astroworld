#!/usr/bin/sh
echo Commit message?
read message
git add .
git commit -m "$message"
git push
git push --tags
