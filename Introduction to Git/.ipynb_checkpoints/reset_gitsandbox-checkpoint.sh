# The following code will reset the ds_gitsandbox to the original 
# main, treasure and translate branches with no changes applied to the 
# translate branch. 

# Clone the repository 
git clone https://github.com/NISR-analysis/ds-gitsandbox.git

# Enter the repository 
cd ds-gitsandbox

# Push main at commit 
git checkout main
git reset --hard eaa00e4
git push --force

# Push treasure at commit 
git checkout treasure
git reset --hard 945c1d8
git push --force 

# Push translate at commit 
git checkout translate
git reset --hard f4c892c
git push --force

# Delete remote branches
# List remote branches in the repository that are not translate, treasure or main
git branch -a | grep -Ev "main|remotes/origin/(?:translate$|treasure$|main$)" |  while read -r line ; do
    git push origin --delete $(echo $line | sed -nr 's/remotes\/origin\/(.*)/\1/p')
done

# Go up one level
cd ..

# Remove repository
rm -rf ds-gitsandbox