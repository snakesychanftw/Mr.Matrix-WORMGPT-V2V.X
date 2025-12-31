#!/usr/bin/env python3
"""
StakeUS GLD Coin Staking Cash Conversion Script
A comprehensive tool for calculating staking rewards and cash conversions for GLD tokens
"""

import sys
from datetime import datetime, timedelta
from decimal import Decimal, getcontext

# Set precision for decimal calculations (28 for financial accuracy)
getcontext().prec = 28


class StakeUSGLDConverter:
    """
    StakeUS GLD Coin Staking Calculator and Cash Converter
    """
    
    def __init__(self):
        self.gld_price_usd = None  # GLD price in USD (must be set before operations)
        # Note: Exchange rates are static and should be updated regularly for accuracy
        self.conversion_rates = {
            'USD': Decimal('1.0'),
            'EUR': Decimal('0.92'),  # Update regularly
            'GBP': Decimal('0.79'),  # Update regularly
            'JPY': Decimal('149.50'),  # Update regularly
            'AUD': Decimal('1.52'),  # Update regularly
            'CAD': Decimal('1.36'),  # Update regularly
        }
        
    def set_gld_price(self, price_usd):
        """Set the current GLD token price in USD"""
        try:
            self.gld_price_usd = Decimal(str(price_usd))
            print(f"✓ GLD Price set to: ${self.gld_price_usd} USD")
            return True
        except (ValueError, TypeError):
            print("✗ Error: Invalid price value")
            return False
    
    def gld_to_cash(self, gld_amount, currency='USD'):
        """Convert GLD tokens to cash value in specified currency"""
        try:
            if self.gld_price_usd is None:
                print("✗ Error: GLD price not set")
                return None
            
            gld_amount = Decimal(str(gld_amount))
            if currency not in self.conversion_rates:
                print(f"✗ Error: Currency {currency} not supported")
                return None
            
            usd_value = gld_amount * self.gld_price_usd
            converted_value = usd_value * self.conversion_rates[currency]
            
            return converted_value
        except (ValueError, TypeError):
            print("✗ Error: Invalid GLD amount")
            return None
    
    def cash_to_gld(self, cash_amount, currency='USD'):
        """Convert cash value to GLD tokens"""
        try:
            if self.gld_price_usd is None or self.gld_price_usd == 0:
                print("✗ Error: GLD price not set")
                return None
            
            cash_amount = Decimal(str(cash_amount))
            if currency not in self.conversion_rates:
                print(f"✗ Error: Currency {currency} not supported")
                return None
            
            usd_value = cash_amount / self.conversion_rates[currency]
            gld_amount = usd_value / self.gld_price_usd
            
            return gld_amount
        except (ValueError, TypeError, ZeroDivisionError):
            print("✗ Error: Invalid cash amount or conversion rate")
            return None
    
    def calculate_staking_rewards(self, gld_staked, apy_percent, days=365):
        """
        Calculate staking rewards based on APY
        
        Args:
            gld_staked: Amount of GLD tokens staked
            apy_percent: Annual Percentage Yield (e.g., 12.5 for 12.5%)
            days: Number of days to stake (default: 365)
        
        Returns:
            dict with rewards calculation details
        """
        try:
            gld_staked = Decimal(str(gld_staked))
            apy = Decimal(str(apy_percent)) / Decimal('100')
            days = Decimal(str(days))
            
            # Calculate daily reward rate (compound interest)
            daily_rate = (Decimal('1') + apy) ** (Decimal('1') / Decimal('365')) - Decimal('1')
            
            # Calculate final amount with compound interest
            final_amount = gld_staked * ((Decimal('1') + daily_rate) ** days)
            rewards = final_amount - gld_staked
            
            # Calculate cash values
            initial_value_usd = self.gld_to_cash(gld_staked, 'USD')
            final_value_usd = self.gld_to_cash(final_amount, 'USD')
            rewards_value_usd = self.gld_to_cash(rewards, 'USD')
            
            return {
                'initial_gld': gld_staked,
                'final_gld': final_amount,
                'rewards_gld': rewards,
                'initial_value_usd': initial_value_usd,
                'final_value_usd': final_value_usd,
                'rewards_value_usd': rewards_value_usd,
                'apy_percent': apy_percent,
                'days': days,
                'end_date': datetime.now() + timedelta(days=float(days))
            }
        except (ValueError, TypeError):
            print("✗ Error: Invalid staking parameters")
            return None
    
    def display_staking_results(self, results):
        """Display staking calculation results in a formatted way"""
        if not results:
            return
        
        print("\n" + "="*60)
        print("STAKEUS GLD STAKING CALCULATION RESULTS".center(60))
        print("="*60)
        print(f"\nStaking Period: {results['days']} days")
        print(f"APY: {results['apy_percent']}%")
        print(f"Expected End Date: {results['end_date'].strftime('%Y-%m-%d')}")
        print("\n" + "-"*60)
        print("GLD TOKENS:".ljust(30))
        print(f"  Initial Stake:".ljust(30) + f"{results['initial_gld']:.4f} GLD")
        print(f"  Expected Final:".ljust(30) + f"{results['final_gld']:.4f} GLD")
        print(f"  Total Rewards:".ljust(30) + f"{results['rewards_gld']:.4f} GLD")
        print("\n" + "-"*60)
        print("USD VALUE (at current price):".ljust(30))
        print(f"  Initial Value:".ljust(30) + f"${results['initial_value_usd']:.2f} USD")
        print(f"  Expected Final:".ljust(30) + f"${results['final_value_usd']:.2f} USD")
        print(f"  Rewards Value:".ljust(30) + f"${results['rewards_value_usd']:.2f} USD")
        print("="*60 + "\n")
    
    def display_conversion_table(self, gld_amount):
        """Display conversion table for GLD to multiple currencies"""
        print("\n" + "="*60)
        print(f"CONVERSION TABLE: {gld_amount} GLD".center(60))
        print("="*60)
        print(f"{'Currency':<15} {'Symbol':<10} {'Value':>20}")
        print("-"*60)
        
        currency_symbols = {
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'JPY': '¥',
            'AUD': 'A$',
            'CAD': 'C$',
        }
        
        for currency in self.conversion_rates.keys():
            value = self.gld_to_cash(gld_amount, currency)
            if value is not None:
                symbol = currency_symbols.get(currency, currency)
                print(f"{currency:<15} {symbol:<10} {value:>20.2f}")
        
        print("="*60 + "\n")


def print_banner():
    """Print application banner"""
    banner = """
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║        StakeUS GLD Coin Staking Cash Converter            ║
    ║                                                            ║
    ║        Calculate staking rewards and cash conversions     ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """
    print(banner)


def interactive_mode():
    """Run the converter in interactive mode"""
    print_banner()
    
    converter = StakeUSGLDConverter()
    
    # Get GLD price
    while True:
        try:
            price_input = input("\nEnter current GLD token price in USD (e.g., 0.50): $")
            price = float(price_input)
            if price > 0:
                converter.set_gld_price(price)
                break
            else:
                print("✗ Price must be greater than 0")
        except ValueError:
            print("✗ Invalid input. Please enter a valid number.")
    
    while True:
        print("\n" + "="*60)
        print("MAIN MENU")
        print("="*60)
        print("1. Convert GLD to Cash")
        print("2. Convert Cash to GLD")
        print("3. Calculate Staking Rewards")
        print("4. Display Multi-Currency Conversion Table")
        print("5. Update GLD Price")
        print("6. Exit")
        print("="*60)
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == '1':
            # GLD to Cash
            try:
                gld_amount = input("\nEnter GLD amount: ")
                print("\nAvailable currencies: USD, EUR, GBP, JPY, AUD, CAD")
                currency = input("Enter currency (default USD): ").strip().upper() or 'USD'
                
                cash_value = converter.gld_to_cash(gld_amount, currency)
                if cash_value is not None:
                    print(f"\n✓ {gld_amount} GLD = {cash_value:.2f} {currency}")
            except Exception as e:
                print(f"✗ Error: {e}")
        
        elif choice == '2':
            # Cash to GLD
            try:
                cash_amount = input("\nEnter cash amount: ")
                print("\nAvailable currencies: USD, EUR, GBP, JPY, AUD, CAD")
                currency = input("Enter currency (default USD): ").strip().upper() or 'USD'
                
                gld_amount = converter.cash_to_gld(cash_amount, currency)
                if gld_amount is not None:
                    print(f"\n✓ {cash_amount} {currency} = {gld_amount:.4f} GLD")
            except Exception as e:
                print(f"✗ Error: {e}")
        
        elif choice == '3':
            # Calculate Staking Rewards
            try:
                gld_staked = input("\nEnter amount of GLD to stake: ")
                apy = input("Enter APY percentage (e.g., 12.5 for 12.5%): ")
                days = input("Enter staking period in days (default 365): ").strip() or '365'
                
                results = converter.calculate_staking_rewards(gld_staked, apy, days)
                if results:
                    converter.display_staking_results(results)
            except Exception as e:
                print(f"✗ Error: {e}")
        
        elif choice == '4':
            # Display Conversion Table
            try:
                gld_amount = input("\nEnter GLD amount for conversion table: ")
                converter.display_conversion_table(float(gld_amount))
            except Exception as e:
                print(f"✗ Error: {e}")
        
        elif choice == '5':
            # Update GLD Price
            try:
                price_input = input("\nEnter new GLD token price in USD: $")
                price = float(price_input)
                if price > 0:
                    converter.set_gld_price(price)
                else:
                    print("✗ Price must be greater than 0")
            except ValueError:
                print("✗ Invalid input. Please enter a valid number.")
        
        elif choice == '6':
            print("\n✓ Thank you for using StakeUS GLD Converter!")
            print("  Goodbye! 👋\n")
            break
        
        else:
            print("\n✗ Invalid option. Please select 1-6.")


def command_line_mode():
    """Run the converter with command line arguments"""
    if len(sys.argv) < 2:
        print("Usage examples:")
        print("  python stakeus_gld_converter.py --price 0.50 --convert-to-cash 1000 --currency USD")
        print("  python stakeus_gld_converter.py --price 0.50 --convert-to-gld 500 --currency USD")
        print("  python stakeus_gld_converter.py --price 0.50 --stake 5000 --apy 12.5 --days 365")
        print("\nOr run without arguments for interactive mode.")
        return
    
    converter = StakeUSGLDConverter()
    
    # Parse arguments
    args = sys.argv[1:]
    i = 0
    price_set = False
    
    while i < len(args):
        arg = args[i]
        
        if arg == '--price' and i + 1 < len(args):
            converter.set_gld_price(args[i + 1])
            price_set = True
            i += 2
        elif arg == '--convert-to-cash' and i + 1 < len(args):
            gld_amount = args[i + 1]
            currency = 'USD'
            # Check if we have both --currency flag and its value
            if i + 2 < len(args) and args[i + 2] == '--currency' and i + 3 < len(args):
                currency = args[i + 3]
                i += 4
            else:
                i += 2
            
            if price_set:
                cash_value = converter.gld_to_cash(gld_amount, currency)
                if cash_value is not None:
                    print(f"\n{gld_amount} GLD = {cash_value:.2f} {currency}\n")
        elif arg == '--convert-to-gld' and i + 1 < len(args):
            cash_amount = args[i + 1]
            currency = 'USD'
            # Check if we have both --currency flag and its value
            if i + 2 < len(args) and args[i + 2] == '--currency' and i + 3 < len(args):
                currency = args[i + 3]
                i += 4
            else:
                i += 2
            
            if price_set:
                gld_amount = converter.cash_to_gld(cash_amount, currency)
                if gld_amount is not None:
                    print(f"\n{cash_amount} {currency} = {gld_amount:.4f} GLD\n")
        elif arg == '--stake' and i + 1 < len(args):
            gld_staked = args[i + 1]
            apy = None
            days = 365
            
            # Check if we have both --apy flag and its value
            if i + 2 < len(args) and args[i + 2] == '--apy' and i + 3 < len(args):
                apy = args[i + 3]
                i += 4
                
                # Check if we have both --days flag and its value
                if i < len(args) and args[i] == '--days' and i + 1 < len(args):
                    days = args[i + 1]
                    i += 2
            else:
                i += 2
            
            if price_set and apy:
                results = converter.calculate_staking_rewards(gld_staked, apy, days)
                if results:
                    converter.display_staking_results(results)
        else:
            i += 1


def main():
    """Main entry point"""
    if len(sys.argv) == 1:
        # No arguments provided, run in interactive mode
        interactive_mode()
    else:
        # Arguments provided, run in command line mode
        command_line_mode()


if __name__ == "__main__":
    main()
