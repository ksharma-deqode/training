git checkout -b temp_merge branch1

git merge --no-commit --no-ff branch2

out=
echo OK

git merge --abort
git checkout -
git branch -D temp_merge

