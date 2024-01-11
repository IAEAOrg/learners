#!/bin/sh

echo "Building hugo content ..."

echo "Ensure themes folder is empty"
rm -rf /src/themes/learners

echo "Download theme ($LEARNERS_GITHUB_THEME_BRANCH)"
wget -q $LEARNERS_GITHUB_THEME_REPO/archive/refs/heads/$LEARNERS_GITHUB_THEME_BRANCH.zip -O /tmp/learners.zip

echo "Unpack theme to themes folder"
unzip -o -qq /tmp/learners.zip -d /src/themes/

echo "Ensure correct folder name"
mv /src/themes/*theme /src/themes/learners

echo "Remove zip file"
rm /tmp/learners.zip

cd /src/themes/learners

# Check if LEARNERS_BASE_URL is set and not empty
LEARNERS_URL="$LEARNERS_BASE_URL/api"
# Remove leading and trailing slashes from LEARNERS_BASE_URL
LEARNERS_URL=$(echo "$LEARNERS_URL" | sed 's#^/*##;s#/*$##')

# Use the variable as needed
echo "LEARNERS_URL is set to: $LEARNERS_URL"

python3 ./build.py -d /src/public -c /src/docker/config.yml -b "$LEARNERS_URL"
