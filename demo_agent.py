#!/usr/bin/env python3
"""
Mr. Matrix Cloudflare Agent - Interactive Demo
===============================================
This script demonstrates the capabilities of the Cloudflare agent
without requiring actual API credentials.
"""

from colorama import Fore, Style, init
import time

init(autoreset=True)


def print_header():
    """Print demo header"""
    print(f"""
{Fore.GREEN}╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║   MR. MATRIX CLOUDFLARE AUTOMATED AGENT - DEMO                 ║
║   ============================================                 ║
║                                                                ║
║   This demo shows what the agent can do!                       ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
""")


def simulate_command(command, description):
    """Simulate executing a command"""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Command: {Style.RESET_ALL}{command}")
    print(f"{Fore.CYAN}Description: {description}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    time.sleep(0.5)


def demo_list_zones():
    """Demo listing zones"""
    simulate_command("list zones", "View all domains in your Cloudflare account")
    
    print(f"{Fore.CYAN}[INFO] Fetching zones from Cloudflare...{Style.RESET_ALL}")
    time.sleep(0.3)
    print(f"{Fore.GREEN}[SUCCESS] Found 3 zone(s){Style.RESET_ALL}\n")
    
    print(f"{Fore.CYAN}╔══════════════════════════════════════════╗")
    print(f"║         CLOUDFLARE ZONES                 ║")
    print(f"╚══════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    zones = [
        ("example.com", "active"),
        ("mysite.net", "active"),
        ("testdomain.org", "pending")
    ]
    
    for name, status in zones:
        status_icon = f"{Fore.GREEN}✓{Style.RESET_ALL}" if status == "active" else f"{Fore.YELLOW}◐{Style.RESET_ALL}"
        print(f"  {status_icon} {name}")
    print()


def demo_list_dns():
    """Demo listing DNS records"""
    simulate_command(
        "list dns records for example.com",
        "View all DNS records for a specific domain"
    )
    
    print(f"{Fore.CYAN}[INFO] Fetching DNS records for example.com...{Style.RESET_ALL}")
    time.sleep(0.3)
    print(f"{Fore.GREEN}[SUCCESS] Found 5 DNS record(s){Style.RESET_ALL}\n")
    
    print(f"{Fore.CYAN}╔══════════════════════════════════════════╗")
    print(f"║         DNS RECORDS FOR EXAMPLE.COM      ║")
    print(f"╚══════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    records = [
        ("A", "example.com", "192.0.2.1", True),
        ("A", "api.example.com", "192.0.2.10", False),
        ("CNAME", "www.example.com", "example.com", True),
        ("MX", "example.com", "mail.example.com", False),
        ("TXT", "example.com", "v=spf1 include:_spf.example.com ~all", False),
    ]
    
    for rec_type, name, content, proxied in records:
        proxy_icon = f"{Fore.YELLOW}☁{Style.RESET_ALL}" if proxied else "  "
        print(f"  {proxy_icon} {rec_type:<6} {name:<30} → {content}")
    print()


def demo_create_dns():
    """Demo creating a DNS record"""
    simulate_command(
        "create dns record for example.com type A name api content 192.0.2.100",
        "Add a new DNS record to your domain"
    )
    
    print(f"{Fore.CYAN}[INFO] Creating DNS record: api.example.com (A) -> 192.0.2.100{Style.RESET_ALL}")
    time.sleep(0.5)
    print(f"{Fore.GREEN}[SUCCESS] DNS record created successfully: abc123def456{Style.RESET_ALL}\n")


def demo_purge_cache():
    """Demo purging cache"""
    simulate_command(
        "purge cache for example.com",
        "Clear all cached content for instant updates"
    )
    
    print(f"{Fore.CYAN}[INFO] Purging all cache for example.com...{Style.RESET_ALL}")
    time.sleep(0.7)
    print(f"{Fore.GREEN}[SUCCESS] Cache purged successfully{Style.RESET_ALL}\n")


def demo_dev_mode():
    """Demo development mode"""
    simulate_command(
        "enable dev mode for example.com",
        "Bypass cache for 3 hours (great for testing)"
    )
    
    print(f"{Fore.CYAN}[INFO] Enabling development mode for example.com...{Style.RESET_ALL}")
    time.sleep(0.4)
    print(f"{Fore.GREEN}[SUCCESS] Development mode enabled{Style.RESET_ALL}\n")


def demo_settings():
    """Demo viewing settings"""
    simulate_command(
        "show settings for example.com",
        "View all configuration settings for your domain"
    )
    
    print(f"{Fore.CYAN}[INFO] Fetching zone settings for example.com...{Style.RESET_ALL}")
    time.sleep(0.3)
    print(f"{Fore.GREEN}[SUCCESS] Retrieved 42 settings{Style.RESET_ALL}\n")
    
    print(f"{Fore.CYAN}╔══════════════════════════════════════════╗")
    print(f"║         SETTINGS FOR EXAMPLE.COM         ║")
    print(f"╚══════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    settings = [
        ("ssl", "full"),
        ("always_use_https", "on"),
        ("automatic_https_rewrites", "on"),
        ("min_tls_version", "1.2"),
        ("security_level", "medium"),
        ("cache_level", "aggressive"),
    ]
    
    for key, value in settings:
        print(f"  {key:<30} : {value}")
    print(f"  {Fore.YELLOW}... and 36 more settings{Style.RESET_ALL}\n")


def demo_natural_language():
    """Demo natural language understanding"""
    print(f"\n{Fore.MAGENTA}╔════════════════════════════════════════════════════════════════╗")
    print(f"║         NATURAL LANGUAGE COMMAND EXAMPLES                      ║")
    print(f"╚════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    examples = [
        "list all my domains",
        "show me the DNS records for example.com",
        "add an A record named api pointing to 192.0.2.50 for example.com",
        "clear the cache for mysite.net",
        "turn on development mode for example.com",
        "what are the firewall rules for mysite.net",
    ]
    
    print(f"{Fore.CYAN}The agent understands natural language! Try commands like:{Style.RESET_ALL}\n")
    for example in examples:
        print(f"  {Fore.GREEN}•{Style.RESET_ALL} {example}")
    print()


def main():
    """Run the demo"""
    print_header()
    
    print(f"{Fore.CYAN}This is a demonstration of the Mr. Matrix Cloudflare Agent.")
    print(f"No actual API calls are made during this demo.{Style.RESET_ALL}\n")
    
    input(f"{Fore.YELLOW}Press Enter to start the demo...{Style.RESET_ALL}")
    
    # Run demos
    demo_list_zones()
    demo_list_dns()
    demo_create_dns()
    demo_purge_cache()
    demo_dev_mode()
    demo_settings()
    demo_natural_language()
    
    # Summary
    print(f"\n{Fore.GREEN}╔════════════════════════════════════════════════════════════════╗")
    print(f"║                     DEMO COMPLETE!                             ║")
    print(f"╚════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    print(f"{Fore.CYAN}Key Features:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Natural language command understanding")
    print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Zone and DNS management")
    print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Cache control")
    print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Settings and firewall management")
    print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Beautiful, colorful output")
    print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Fully automated - just say what you want!\n")
    
    print(f"{Fore.YELLOW}To use the real agent:{Style.RESET_ALL}")
    print(f"  1. Set CLOUDFLARE_API_TOKEN environment variable")
    print(f"  2. Run: python3 mr_matrix_cloudflare.py")
    print(f"  3. Start managing your Cloudflare domains!\n")
    
    print(f"{Fore.CYAN}Documentation:{Style.RESET_ALL}")
    print(f"  • QUICKSTART.md - Quick start guide")
    print(f"  • CLOUDFLARE_AGENT_README.md - Full documentation")
    print(f"  • example_usage.py - Code examples\n")


if __name__ == '__main__':
    main()
