# tail the most recent log file
tail -f "logs/$(ls -Lt ./logs | head -n1)"
