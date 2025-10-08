#!/bin/bash
# Demo script to showcase Stock Assistant MVP features

echo "=========================================="
echo "Stock Assistant MVP - Demo"
echo "=========================================="
echo ""

echo "1. Getting information about Apple Inc. (AAPL)"
echo "Command: python stock_assistant.py info AAPL"
echo ""
python3 stock_assistant.py info AAPL

echo ""
echo "2. Calculating portfolio value"
echo "Command: python stock_assistant.py portfolio AAPL:10 GOOGL:5 MSFT:3"
echo ""
python3 stock_assistant.py portfolio AAPL:10 GOOGL:5 MSFT:3

echo ""
echo "3. Comparing stocks"
echo "Command: python stock_assistant.py compare AAPL GOOGL MSFT"
echo ""
python3 stock_assistant.py compare AAPL GOOGL MSFT

echo ""
echo "Demo completed!"
echo "Run 'python stock_assistant.py help' for more information"
