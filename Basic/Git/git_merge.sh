git init -b main
git commit --allow-empty -m 0
git branch dev
git checkout dev
git commit --allow-empty -m 1
git commit --allow-empty -m 2

git merge main

git log --graph --oneline --all
