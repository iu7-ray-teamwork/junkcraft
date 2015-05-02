rm -rf out || exit 0;
mkdir out;

GH_REPO="@github.com/iu7-ray-teamwork/junkcraft.git"
FULL_REPO="https://$GH_TOKEN$GH_REPO"

cd out
git init
git config user.name "Travis CI"
git config user.email "travis"

for module in "engine" "engine._Surface" "engine.math" "engine.math._Vector" "engine.math._Matrix";
  do python -m pydoc -w $module;
done

git add .
git commit -m "Generated docs"
git push --force --quiet $FULL_REPO master:gh-pages
