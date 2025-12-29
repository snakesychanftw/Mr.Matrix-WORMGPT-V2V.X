#!/usr/bin/env python3
"""
Example usage of the Cloudflare Agent
======================================
This script demonstrates how to use the Cloudflare agent programmatically.
"""

from cloudflare_agent import CloudflareAgent
import os


def main():
    """Example usage of the Cloudflare agent"""
    
    # Check for API token
    if not os.getenv('CLOUDFLARE_API_TOKEN'):
        print("Please set CLOUDFLARE_API_TOKEN environment variable")
        print("Example: export CLOUDFLARE_API_TOKEN='your-token-here'")
        return
    
    # Initialize agent
    print("Initializing Cloudflare Agent...")
    agent = CloudflareAgent()
    
    # Example 1: List all zones
    print("\n" + "="*60)
    print("Example 1: List all zones")
    print("="*60)
    zones = agent.get_zones()
    print(f"Found {len(zones)} zone(s)")
    
    if not zones:
        print("No zones found. Please add a domain to your Cloudflare account first.")
        return
    
    # Use the first zone for examples
    example_domain = zones[0]['name']
    print(f"\nUsing domain: {example_domain}")
    
    # Example 2: List DNS records
    print("\n" + "="*60)
    print("Example 2: List DNS records")
    print("="*60)
    records = agent.list_dns_records(example_domain)
    print(f"Found {len(records)} DNS record(s)")
    
    # Example 3: Get zone settings
    print("\n" + "="*60)
    print("Example 3: Get zone settings")
    print("="*60)
    settings = agent.get_zone_settings(example_domain)
    print(f"Retrieved {len(settings)} setting(s)")
    
    # Example 4: Using natural language commands
    print("\n" + "="*60)
    print("Example 4: Natural language commands")
    print("="*60)
    
    # List zones using natural language
    print("\nCommand: 'list zones'")
    agent.execute_command('list zones')
    
    # List DNS records using natural language
    print(f"\nCommand: 'list dns records for {example_domain}'")
    agent.execute_command(f'list dns records for {example_domain}')
    
    # Example 5: Create and delete a DNS record (commented out for safety)
    print("\n" + "="*60)
    print("Example 5: DNS record management (demonstration only)")
    print("="*60)
    print("""
    # To create a DNS record:
    agent.create_dns_record(
        domain='example.com',
        record_type='A',
        name='test',
        content='192.0.2.1',
        proxied=False
    )
    
    # To delete a DNS record:
    agent.delete_dns_record(
        domain='example.com',
        record_name='test'
    )
    
    # Using natural language:
    agent.execute_command('create dns record for example.com type A name test content 192.0.2.1')
    agent.execute_command('delete dns record test from example.com')
    """)
    
    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60)


if __name__ == '__main__':
    main()
