#!/bin/bash
echo "Stopping all processes..."
kill 812
kill 813
# Localtunnel will be stopped by Ctrl+C in the main script
rm stop_game.sh
echo "Done."
