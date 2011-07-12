#!/bin/bash

source ~/Sites/goodsie/env/bin/activate
cd ~/Projects/oauth2app
git checkout develop
cd docs
make html
cp -r _build/html ~/Desktop/oauth2appdocs
cd ~/Projects/oauth2app/
git checkout gh-pages
cp -r ~/Desktop/oauth2appdocs/* .
rm -rf ~/Desktop/oauth2appdocs
git add *
git commit -a -m "Automated documentation build."
git push origin gh-pages
git checkout develop