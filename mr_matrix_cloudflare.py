#!/usr/bin/env python3
"""
Mr. Matrix Cloudflare Agent - Interactive CLI
==============================================
Interactive command-line interface for the Cloudflare automated agent.
"""

import os
import sys
from cloudflare_agent import CloudflareAgent
from colorama import Fore, Style, init

init(autoreset=True)


def print_banner():
    """Print the Mr. Matrix banner"""
    banner = f"""
{Fore.GREEN}
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║   ███╗   ███╗██████╗      ███╗   ███╗ █████╗ ████████╗██████╗ ██╗██╗  ██╗
║   ████╗ ████║██╔══██╗     ████╗ ████║██╔══██╗╚══██╔══╝██╔══██╗██║╚██╗██╔╝
║   ██╔████╔██║██████╔╝     ██╔████╔██║███████║   ██║   ██████╔╝██║ ╚███╔╝ 
║   ██║╚██╔╝██║██╔══██╗     ██║╚██╔╝██║██╔══██║   ██║   ██╔══██╗██║ ██╔██╗ 
║   ██║ ╚═╝ ██║██║  ██║     ██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║██║██╔╝ ██╗
║   ╚═╝     ╚═╝╚═╝  ╚═╝     ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
║                                                                ║
║              CLOUDFLARE AUTOMATED AGENT V1.0                   ║
║              ================================                   ║
║                                                                ║
║    Your automated assistant for Cloudflare management         ║
║    Just say what you want to do, and I'll make it happen!     ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    print(banner)


def print_help():
    """Print help information"""
    help_text = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                     AVAILABLE COMMANDS                       ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.YELLOW}Zone Management:{Style.RESET_ALL}
  • list zones                        - List all zones in your account
  • show zones                         - Same as list zones

{Fore.YELLOW}DNS Management:{Style.RESET_ALL}
  • list dns records for <domain>     - List all DNS records
  • show records for <domain>          - Same as list dns records
  • create dns record for <domain> type <TYPE> name <NAME> content <IP/DOMAIN>
                                       - Create a new DNS record
  • delete dns record <name> from <domain>
                                       - Delete a DNS record

{Fore.YELLOW}Cache Management:{Style.RESET_ALL}
  • purge cache for <domain>          - Purge all cache for domain
  • clear cache for <domain>           - Same as purge cache

{Fore.YELLOW}Settings:{Style.RESET_ALL}
  • show settings for <domain>        - Display zone settings
  • enable dev mode for <domain>      - Enable development mode
  • disable dev mode for <domain>     - Disable development mode

{Fore.YELLOW}Firewall:{Style.RESET_ALL}
  • list firewall rules for <domain>  - List firewall rules
  • show firewall for <domain>         - Same as list firewall rules

{Fore.YELLOW}General:{Style.RESET_ALL}
  • help                               - Show this help message
  • exit, quit                         - Exit the agent

{Fore.GREEN}Examples:{Style.RESET_ALL}
  > list zones
  > list dns records for example.com
  > create dns record for example.com type A name www content 192.0.2.1
  > purge cache for example.com
  > enable dev mode for example.com

{Fore.CYAN}═══════════════════════════════════════════════════════════════{Style.RESET_ALL}
"""
    print(help_text)


def setup_credentials():
    """Guide user through credential setup"""
    print(f"\n{Fore.YELLOW}╔══════════════════════════════════════════════════════════════╗")
    print(f"║              CLOUDFLARE CREDENTIALS SETUP                ║")
    print(f"╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    print("To use this agent, you need Cloudflare API credentials.\n")
    print(f"{Fore.CYAN}Option 1 (Recommended):{Style.RESET_ALL} API Token")
    print("  1. Go to: https://dash.cloudflare.com/profile/api-tokens")
    print("  2. Click 'Create Token'")
    print("  3. Use 'Edit zone DNS' template or create custom token")
    print("  4. Copy the token\n")
    
    print(f"{Fore.CYAN}Option 2:{Style.RESET_ALL} Global API Key (Legacy)")
    print("  1. Go to: https://dash.cloudflare.com/profile/api-tokens")
    print("  2. View your Global API Key")
    print("  3. Also need your Cloudflare account email\n")
    
    print(f"{Fore.GREEN}Setting credentials:{Style.RESET_ALL}")
    print("  Set environment variable:")
    print(f"    export CLOUDFLARE_API_TOKEN='your-token-here'\n")
    
    print("  Or create a .env file:")
    print("    CLOUDFLARE_API_TOKEN=your-token-here\n")
    
    input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


def main():
    """Main interactive CLI loop"""
    print_banner()
    
    # Check for credentials
    if not os.getenv('CLOUDFLARE_API_TOKEN') and not (os.getenv('CLOUDFLARE_EMAIL') and os.getenv('CLOUDFLARE_API_KEY')):
        print(f"{Fore.RED}⚠ No Cloudflare credentials found!{Style.RESET_ALL}\n")
        setup_credentials()
        
        # Check again
        if not os.getenv('CLOUDFLARE_API_TOKEN') and not (os.getenv('CLOUDFLARE_EMAIL') and os.getenv('CLOUDFLARE_API_KEY')):
            print(f"\n{Fore.RED}Error: Still no credentials found. Please set them and try again.{Style.RESET_ALL}")
            print(f"Example: export CLOUDFLARE_API_TOKEN='your-token-here'\n")
            sys.exit(1)
    
    # Initialize agent
    try:
        agent = CloudflareAgent()
        print(f"\n{Fore.GREEN}✓ Agent initialized successfully!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Type 'help' for available commands or 'exit' to quit.{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"\n{Fore.RED}Failed to initialize agent: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please check your credentials and try again.{Style.RESET_ALL}\n")
        sys.exit(1)
    
    # Main loop
    while True:
        try:
            # Get user input
            command = input(f"{Fore.MAGENTA}Mr. Matrix >{Style.RESET_ALL} ").strip()
            
            # Skip empty commands
            if not command:
                continue
            
            # Handle exit
            if command.lower() in ['exit', 'quit', 'q']:
                print(f"\n{Fore.GREEN}Goodbye! Mr. Matrix signing off... 👋{Style.RESET_ALL}\n")
                break
            
            # Handle help
            if command.lower() in ['help', '?', 'h']:
                print_help()
                continue
            
            # Execute command
            print()  # New line for better formatting
            agent.execute_command(command)
            print()  # New line after execution
            
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Interrupted by user. Type 'exit' to quit or continue entering commands.{Style.RESET_ALL}\n")
        except Exception as e:
            print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}\n")


if __name__ == '__main__':
    main()
