#!/usr/bin/env python3
"""
Stock Assistant MVP - A simple command-line tool for stock information
"""

import sys
import json
from datetime import datetime
from typing import Dict, Optional


class StockAssistant:
    """A simple stock assistant that provides stock information and analysis."""
    
    def __init__(self):
        self.stock_data = {}
        
    def get_stock_info(self, symbol: str) -> Optional[Dict]:
        """
        Get basic information about a stock.
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
            
        Returns:
            Dictionary containing stock information or None if not found
        """
        # In a real implementation, this would fetch from an API
        # For MVP, we'll use sample data
        sample_stocks = {
            'AAPL': {
                'name': 'Apple Inc.',
                'symbol': 'AAPL',
                'price': 175.50,
                'currency': 'USD',
                'market_cap': '2.75T',
                'pe_ratio': 28.5,
                'dividend_yield': 0.52
            },
            'GOOGL': {
                'name': 'Alphabet Inc.',
                'symbol': 'GOOGL',
                'price': 142.30,
                'currency': 'USD',
                'market_cap': '1.80T',
                'pe_ratio': 25.8,
                'dividend_yield': 0.0
            },
            'MSFT': {
                'name': 'Microsoft Corporation',
                'symbol': 'MSFT',
                'price': 378.90,
                'currency': 'USD',
                'market_cap': '2.82T',
                'pe_ratio': 35.2,
                'dividend_yield': 0.75
            }
        }
        
        return sample_stocks.get(symbol.upper())
    
    def display_stock_info(self, symbol: str):
        """Display formatted stock information."""
        info = self.get_stock_info(symbol)
        
        if not info:
            print(f"\n❌ Stock symbol '{symbol}' not found in sample data.")
            print("Available symbols: AAPL, GOOGL, MSFT")
            return
        
        print(f"\n{'='*60}")
        print(f"📊 Stock Information for {info['name']}")
        print(f"{'='*60}")
        print(f"Symbol:          {info['symbol']}")
        print(f"Current Price:   ${info['price']:.2f} {info['currency']}")
        print(f"Market Cap:      {info['market_cap']}")
        print(f"P/E Ratio:       {info['pe_ratio']}")
        print(f"Dividend Yield:  {info['dividend_yield']}%")
        print(f"{'='*60}\n")
    
    def calculate_portfolio_value(self, holdings: Dict[str, float]) -> float:
        """
        Calculate total portfolio value.
        
        Args:
            holdings: Dictionary of {symbol: shares} pairs
            
        Returns:
            Total portfolio value in USD
        """
        total_value = 0.0
        
        print("\n📈 Portfolio Analysis")
        print(f"{'='*60}")
        
        for symbol, shares in holdings.items():
            info = self.get_stock_info(symbol)
            if info:
                value = info['price'] * shares
                total_value += value
                print(f"{symbol:6} | {shares:8.2f} shares @ ${info['price']:8.2f} = ${value:10.2f}")
            else:
                print(f"{symbol:6} | Not found in database")
        
        print(f"{'='*60}")
        print(f"Total Portfolio Value: ${total_value:,.2f}")
        print(f"{'='*60}\n")
        
        return total_value
    
    def compare_stocks(self, symbols: list):
        """Compare multiple stocks side by side."""
        print("\n📊 Stock Comparison")
        print(f"{'='*80}")
        print(f"{'Symbol':<10} {'Name':<25} {'Price':>12} {'P/E':>8} {'Div Yield':>10}")
        print(f"{'-'*80}")
        
        for symbol in symbols:
            info = self.get_stock_info(symbol)
            if info:
                print(f"{info['symbol']:<10} {info['name']:<25} ${info['price']:>11.2f} "
                      f"{info['pe_ratio']:>8.1f} {info['dividend_yield']:>9.2f}%")
            else:
                print(f"{symbol:<10} Not found")
        
        print(f"{'='*80}\n")


def print_help():
    """Print help information."""
    help_text = """
Stock Assistant MVP - Command Line Interface

Usage:
    python stock_assistant.py <command> [arguments]

Commands:
    info <SYMBOL>              Get information about a stock
                              Example: python stock_assistant.py info AAPL
    
    portfolio <SYMBOL:SHARES>  Calculate portfolio value
                              Example: python stock_assistant.py portfolio AAPL:10 GOOGL:5
    
    compare <SYMBOLS>          Compare multiple stocks
                              Example: python stock_assistant.py compare AAPL GOOGL MSFT
    
    help                      Display this help message

Sample Symbols:
    AAPL  - Apple Inc.
    GOOGL - Alphabet Inc.
    MSFT  - Microsoft Corporation

Note: This is an MVP with sample data. In production, it would connect to a real stock API.
"""
    print(help_text)


def main():
    """Main entry point for the stock assistant."""
    assistant = StockAssistant()
    
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'help':
        print_help()
    
    elif command == 'info':
        if len(sys.argv) < 3:
            print("❌ Error: Please provide a stock symbol")
            print("Usage: python stock_assistant.py info <SYMBOL>")
            return
        symbol = sys.argv[2]
        assistant.display_stock_info(symbol)
    
    elif command == 'portfolio':
        if len(sys.argv) < 3:
            print("❌ Error: Please provide holdings")
            print("Usage: python stock_assistant.py portfolio <SYMBOL:SHARES> [<SYMBOL:SHARES> ...]")
            return
        
        holdings = {}
        for arg in sys.argv[2:]:
            try:
                symbol, shares = arg.split(':')
                holdings[symbol.upper()] = float(shares)
            except ValueError:
                print(f"❌ Error: Invalid format '{arg}'. Use SYMBOL:SHARES (e.g., AAPL:10)")
                return
        
        assistant.calculate_portfolio_value(holdings)
    
    elif command == 'compare':
        if len(sys.argv) < 3:
            print("❌ Error: Please provide at least one stock symbol")
            print("Usage: python stock_assistant.py compare <SYMBOL> [<SYMBOL> ...]")
            return
        
        symbols = [s.upper() for s in sys.argv[2:]]
        assistant.compare_stocks(symbols)
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Run 'python stock_assistant.py help' for usage information")


if __name__ == '__main__':
    main()
