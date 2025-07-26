#!/bin/bash
# scripts/release.sh

VERSION=$1
if [ -z "$VERSION" ]; then
  echo "Usage: ./release.sh <version>"
  exit 1
fi

echo "🚀 Releasing Genesis Engine v$VERSION"

# Update version in all packages
repos=("core" "cli" "agents" "templates" "web")

for repo in "${repos[@]}"; do
  echo "📝 Updating version in genesis-engine-$repo..."
  cd "genesis-engine-$repo"
  npm version "$VERSION" --no-git-tag-version
  cd ..
done

echo "✅ Version updated to $VERSION in all repositories"
echo "🔖 Next steps:"
echo "   1. Commit changes in each repository"
echo "   2. Create tags: git tag v$VERSION"
echo "   3. Push tags: git push origin v$VERSION"
