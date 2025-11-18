#!/usr/bin/env bash
# Prints basic system details
echo "Kernel Version:"
uname -r
echo "User:"
whoami
echo "Hardware Info (lscpu | grep 'Virtualization'):"
lscpu | grep -i 'Virtualization' || true
