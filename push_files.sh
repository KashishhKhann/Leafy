#!/bin/bash

# List of important files to keep
FILES=(
    "Leafy.py"
    "config.py"
    "logger.py"
    "utils.py"
    "platform_utils.py"
    "db.py"
    "cache.py"
    "async_ops.py"
    "settings_gui.py"
    "requirements.txt"
    ".env.example"
    ".gitignore"
    "README.md"
    "00_START_HERE.txt"
    "QUICK_START_ADVANCED.md"
    "test_advanced_features.py"
)

echo "Important files to push:"
for file in "${FILES[@]}"; do
    echo "  - $file"
done
