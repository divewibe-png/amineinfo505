
#!/bin/sh
set -eu

nginx
exec python3 /manager.py
