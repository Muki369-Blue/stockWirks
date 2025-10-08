# stockWirks

A simple command-line stock assistant MVP (Minimum Viable Product) for viewing stock information, calculating portfolio values, and comparing stocks.

## Features

- 📊 View detailed stock information
- 💼 Calculate portfolio value with multiple holdings
- 🔍 Compare multiple stocks side by side
- 🚀 Simple command-line interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Muki369-Blue/stockWirks.git
cd stockWirks
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Get Stock Information
View detailed information about a specific stock:
```bash
python stock_assistant.py info AAPL
```

### Calculate Portfolio Value
Calculate the total value of your stock holdings:
```bash
python stock_assistant.py portfolio AAPL:10 GOOGL:5 MSFT:3
```
Format: `SYMBOL:SHARES` (e.g., AAPL:10 means 10 shares of Apple)

### Compare Stocks
Compare multiple stocks side by side:
```bash
python stock_assistant.py compare AAPL GOOGL MSFT
```

### Help
Display help information:
```bash
python stock_assistant.py help
```

## Available Sample Stocks

For this MVP, the following sample stocks are available:
- **AAPL** - Apple Inc.
- **GOOGL** - Alphabet Inc.
- **MSFT** - Microsoft Corporation

## Example Output

```
============================================================
📊 Stock Information for Apple Inc.
============================================================
Symbol:          AAPL
Current Price:   $175.50 USD
Market Cap:      2.75T
P/E Ratio:       28.5
Dividend Yield:  0.52%
============================================================
```

## Future Enhancements

This is an MVP with sample data. Future versions could include:
- Integration with real-time stock APIs (Alpha Vantage, Yahoo Finance, etc.)
- Historical price charts
- Technical indicators (RSI, MACD, Moving Averages)
- Portfolio tracking over time
- Alert notifications for price changes
- Web interface
- Stock screening and filtering

## Configuration

Copy `config.example.ini` to `config.ini` and customize settings:
```bash
cp config.example.ini config.ini
```

## Requirements

- Python 3.7+
- See `requirements.txt` for Python package dependencies

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
