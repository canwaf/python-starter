#!/bin/sh

# Set up pre-push hook to run lint and tests
cat << 'EOF' > .git/hooks/pre-push
#!/bin/sh
poetry run lint || exit 1
poetry run test || exit 1
echo "Pre-push checks passed."
EOF
chmod +x .git/hooks/pre-push

# Set commit message template
if [ -f .gitmessage ]; then
  git config commit.template .gitmessage
fi

# Create and activate virtual environment
python3 -m venv .venv
. .venv/bin/activate

# Install dependencies with poetry
poetry install