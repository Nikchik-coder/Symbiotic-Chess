#!/bin/bash

echo "Starting backend server in the background..."
cd backend
./venv/Scripts/python server.py &
BACKEND_PID=$!
cd ..

echo "Starting frontend server in the background..."
cd frontend
py -m http.server &
FRONTEND_PID=$!
cd ..

echo "Starting localtunnels..."
{
    lt --port 8000 > frontend.url &
    lt --port 5000 > backend.url &
}

echo "Waiting for tunnels to be established..."
while [ ! -s frontend.url ] || [ ! -s backend.url ]; do
    sleep 1
done

FRONTEND_URL=$(cat frontend.url | cut -d' ' -f4)
BACKEND_URL=$(cat backend.url | cut -d' ' -f4)

rm frontend.url backend.url

GAME_URL="$FRONTEND_URL?api=$BACKEND_URL"

echo "--------------------------------------------------"
echo "Your game is ready!"
echo "Share this link with your friend (or open on your mobile):"
echo $GAME_URL
echo "--------------------------------------------------"
echo "Press Ctrl+C in this window to stop all servers."

# Create a stop script
cat <<EOL > stop_game.sh
#!/bin/bash
echo "Stopping all processes..."
kill $BACKEND_PID
kill $FRONTEND_PID
# Localtunnel will be stopped by Ctrl+C in the main script
rm stop_game.sh
echo "Done."
EOL
chmod +x stop_game.sh

# Wait for user to press Ctrl+C to stop the tunnels
wait
./stop_game.sh
