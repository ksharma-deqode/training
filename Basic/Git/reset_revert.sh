git init
echo initial > file.txt
git add file.txt
git commit -m Commit 0

echo content version1 > file.txt
git add file.txt
git commit -m Commit 1

echo content version2 > file.txt
git add file.txt
git commit -m Commit 2

git reset --soft HEAD~1     # Move HEAD only
# git reset --mixed HEAD~1  # Move HEAD + update index
# git reset --hard HEAD~1   # Move HEAD + update index + update working tree

git revert --no-edit <commit_id>

echo HEAD Commit ID: 9c53232
echo Index Content: 
echo Working Directory Content: 

