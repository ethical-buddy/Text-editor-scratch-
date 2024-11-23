#!/bin/bash

# Define variables
INSTALL_DIR="$HOME/.local/bin"
SCRIPT_NAME="advanced_notepad"
PYTHON_SCRIPT="advanced_notepad.py"

# Ensure the installation directory exists
mkdir -p "$INSTALL_DIR"

# Copy the Python script to the installation directory
cp "$PYTHON_SCRIPT" "$INSTALL_DIR/$SCRIPT_NAME"

# Make the script executable
chmod +x "$INSTALL_DIR/$SCRIPT_NAME"

# Add the installation directory to PATH if not already present
if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
    echo 'PATH updated. Please restart your terminal or run `source ~/.zshrc`.'
fi

echo "Installation complete! Run '$SCRIPT_NAME' to start the editor."

