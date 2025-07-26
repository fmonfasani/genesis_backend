#!/bin/bash
# scripts/setup-dev.sh

echo "🚀 Setting up Genesis Engine development environment..."

# Clone all repositories
repos=(
  "genesis-engine-core"
  "genesis-engine-cli"
  "genesis-engine-agents"
  "genesis-engine-templates"
  "genesis-engine-web"
)

for repo in "${repos[@]}"; do
  if [ ! -d "$repo" ]; then
    echo "📥 Cloning $repo..."
    git clone "https://github.com/your-org/$repo.git"
  fi
done

# Install dependencies
echo "📦 Installing dependencies..."
for repo in "${repos[@]}"; do
  if [ -d "$repo" ]; then
    echo "Installing dependencies for $repo..."
    cd "$repo"
    npm install
    cd ..
  fi
done

echo "✅ Development environment ready!"
