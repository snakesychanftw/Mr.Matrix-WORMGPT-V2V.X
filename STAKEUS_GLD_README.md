# StakeUS GLD Coin Staking Cash Conversion Script

A comprehensive Python tool for calculating staking rewards and cash conversions for StakeUS GLD tokens.

## Features

- **GLD to Cash Conversion**: Convert GLD tokens to cash value in multiple currencies
- **Cash to GLD Conversion**: Calculate how many GLD tokens you can get with a specific amount of cash
- **Staking Rewards Calculator**: Calculate expected staking rewards based on APY
- **Multi-Currency Support**: Support for USD, EUR, GBP, JPY, AUD, and CAD
- **Interactive Mode**: User-friendly interactive menu system
- **Command-Line Mode**: Quick calculations via command-line arguments

## Installation

No additional dependencies required! The script uses only Python standard library.

```bash
# Make the script executable
chmod +x stakeus_gld_converter.py
```

## Usage

### Interactive Mode

Run the script without arguments for an interactive experience:

```bash
python3 stakeus_gld_converter.py
```

You'll be presented with a menu where you can:
1. Convert GLD to Cash
2. Convert Cash to GLD
3. Calculate Staking Rewards
4. Display Multi-Currency Conversion Table
5. Update GLD Price
6. Exit

### Command-Line Mode

#### Convert GLD to Cash

```bash
python3 stakeus_gld_converter.py --price 0.50 --convert-to-cash 1000 --currency USD
```

Output:
```
✓ GLD Price set to: $0.50 USD
1000 GLD = 500.00 USD
```

#### Convert Cash to GLD

```bash
python3 stakeus_gld_converter.py --price 0.50 --convert-to-gld 500 --currency EUR
```

Output:
```
✓ GLD Price set to: $0.50 USD
500 EUR = 1086.9565 GLD
```

#### Calculate Staking Rewards

```bash
python3 stakeus_gld_converter.py --price 0.50 --stake 5000 --apy 12.5 --days 365
```

Output:
```
✓ GLD Price set to: $0.50 USD

============================================================
          STAKEUS GLD STAKING CALCULATION RESULTS           
============================================================

Staking Period: 365 days
APY: 12.5%
Expected End Date: 2026-12-26

------------------------------------------------------------
GLD TOKENS:                   
  Initial Stake:              5000.0000 GLD
  Expected Final:             5624.9993 GLD
  Total Rewards:              624.9993 GLD

------------------------------------------------------------
USD VALUE (at current price): 
  Initial Value:              $2500.00 USD
  Expected Final:             $2812.50 USD
  Rewards Value:              $312.50 USD
============================================================
```

## Command-Line Arguments

- `--price <value>`: Set the current GLD token price in USD (required for all operations)
- `--convert-to-cash <amount>`: Convert GLD tokens to cash
- `--convert-to-gld <amount>`: Convert cash to GLD tokens
- `--currency <code>`: Specify currency (USD, EUR, GBP, JPY, AUD, CAD) - default: USD
- `--stake <amount>`: Amount of GLD to stake
- `--apy <percentage>`: Annual Percentage Yield (e.g., 12.5 for 12.5%)
- `--days <number>`: Staking period in days - default: 365

## Examples

### Example 1: Quick Conversion Check

```bash
# Check how much 10,000 GLD is worth in different currencies
python3 stakeus_gld_converter.py --price 0.75 --convert-to-cash 10000 --currency USD
python3 stakeus_gld_converter.py --price 0.75 --convert-to-cash 10000 --currency EUR
python3 stakeus_gld_converter.py --price 0.75 --convert-to-cash 10000 --currency GBP
```

### Example 2: Staking Planning

```bash
# Calculate 30-day staking rewards for 2000 GLD at 10% APY
python3 stakeus_gld_converter.py --price 0.60 --stake 2000 --apy 10 --days 30

# Calculate 1-year staking rewards for 10000 GLD at 15% APY
python3 stakeus_gld_converter.py --price 0.60 --stake 10000 --apy 15 --days 365
```

### Example 3: Investment Planning

```bash
# How much GLD can I buy with $1000?
python3 stakeus_gld_converter.py --price 0.45 --convert-to-gld 1000 --currency USD
```

## Features Explained

### Compound Interest Calculation

The staking rewards calculator uses compound interest formulas to provide accurate projections:
- Daily compounding is applied for precise calculations
- APY (Annual Percentage Yield) is used for calculations
- Final amount includes both principal and earned rewards

### Multi-Currency Support

The following currencies are supported with real-time conversion:
- **USD** - United States Dollar ($)
- **EUR** - Euro (€)
- **GBP** - British Pound (£)
- **JPY** - Japanese Yen (¥)
- **AUD** - Australian Dollar (A$)
- **CAD** - Canadian Dollar (C$)

### Precision

The script uses Python's `Decimal` library for high-precision financial calculations, ensuring accurate results for all conversions and calculations.

## Tips

1. **Update GLD Price Regularly**: Cryptocurrency prices are volatile. Always use the current market price for accurate conversions.

2. **Use Interactive Mode for Exploration**: The interactive mode is perfect for exploring different staking scenarios without having to remember command-line arguments.

3. **Staking Calculations Are Estimates**: Actual staking rewards may vary based on network conditions, validator performance, and other factors.

4. **Multiple Calculations**: In interactive mode, you can perform multiple calculations without restarting the script.

## Security Note

This script performs calculations locally and does not connect to any external services or APIs. Your calculations and data remain private on your machine.

## License

This tool is part of the Mr.Matrix-WORMGPT-V2V.X project and is licensed under the MIT License.

## Contributing

Contributions are welcome! Feel free to submit pull requests or report issues.

## Disclaimer

This tool is for informational and planning purposes only. It does not constitute financial advice. Cryptocurrency investments carry risk, and past performance does not guarantee future results. Always do your own research before making investment decisions.
