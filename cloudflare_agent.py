"""
Mr. Matrix Cloudflare Automated Agent
======================================
An automated agent that connects to Cloudflare and helps you perform tasks end-to-end.
Simply say what to do, and the agent will execute it automatically.
"""

import json
import os
import re
from typing import Dict, List, Optional, Any
from cloudflare import Cloudflare
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


class CloudflareAgent:
    """Automated Cloudflare agent for task execution"""
    
    def __init__(self, api_token: Optional[str] = None, email: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize the Cloudflare agent.
        
        Args:
            api_token: Cloudflare API token (preferred method)
            email: Cloudflare account email (legacy auth)
            api_key: Cloudflare API key (legacy auth)
        """
        self.api_token = api_token or os.getenv('CLOUDFLARE_API_TOKEN')
        self.email = email or os.getenv('CLOUDFLARE_EMAIL')
        self.api_key = api_key or os.getenv('CLOUDFLARE_API_KEY')
        
        # Initialize Cloudflare API client
        if self.api_token:
            self.cf = Cloudflare(api_token=self.api_token)
        elif self.email and self.api_key:
            self.cf = Cloudflare(api_email=self.email, api_key=self.api_key)
        else:
            raise ValueError("No Cloudflare credentials provided. Set CLOUDFLARE_API_TOKEN environment variable or pass credentials.")
        
        self.zones_cache = {}
        
    def log_info(self, message: str):
        """Log informational message"""
        print(f"{Fore.CYAN}[INFO] {message}{Style.RESET_ALL}")
    
    def log_success(self, message: str):
        """Log success message"""
        print(f"{Fore.GREEN}[SUCCESS] {message}{Style.RESET_ALL}")
    
    def log_error(self, message: str):
        """Log error message"""
        print(f"{Fore.RED}[ERROR] {message}{Style.RESET_ALL}")
    
    def log_warning(self, message: str):
        """Log warning message"""
        print(f"{Fore.YELLOW}[WARNING] {message}{Style.RESET_ALL}")
    
    def get_zones(self, force_refresh: bool = False) -> List[Dict]:
        """
        Get all zones (domains) in the Cloudflare account.
        
        Args:
            force_refresh: Force refresh of zones cache
            
        Returns:
            List of zone dictionaries
        """
        if not self.zones_cache or force_refresh:
            try:
                self.log_info("Fetching zones from Cloudflare...")
                zones_response = self.cf.zones.list()
                zones = list(zones_response)
                self.zones_cache = {zone.name: zone for zone in zones}
                self.log_success(f"Found {len(zones)} zone(s)")
            except Exception as e:
                self.log_error(f"Failed to fetch zones: {e}")
                return []
        return list(self.zones_cache.values())
    
    def find_zone(self, domain: str) -> Optional[Any]:
        """
        Find a zone by domain name.
        
        Args:
            domain: Domain name to search for
            
        Returns:
            Zone object if found, None otherwise
        """
        zones = self.get_zones()
        
        # Exact match
        for zone in zones:
            if zone.name.lower() == domain.lower():
                return zone
        
        # Partial match
        for zone in zones:
            if domain.lower() in zone.name.lower():
                return zone
        
        return None
    
    def list_dns_records(self, domain: str, record_type: Optional[str] = None) -> List[Dict]:
        """
        List DNS records for a domain.
        
        Args:
            domain: Domain name
            record_type: Filter by record type (A, AAAA, CNAME, MX, TXT, etc.)
            
        Returns:
            List of DNS record dictionaries
        """
        zone = self.find_zone(domain)
        if not zone:
            self.log_error(f"Zone not found for domain: {domain}")
            return []
        
        try:
            zone_id = zone.id
            self.log_info(f"Fetching DNS records for {domain}...")
            
            params = {}
            if record_type:
                params['type'] = record_type.upper()
            
            records_response = self.cf.dns.records.list(zone_id=zone_id, **params)
            # Use model_dump() if available (Pydantic v2), fallback to vars()
            records = [
                record.model_dump() if hasattr(record, 'model_dump') else vars(record) 
                for record in records_response
            ]
            self.log_success(f"Found {len(records)} DNS record(s)")
            return records
        except Exception as e:
            self.log_error(f"Failed to fetch DNS records: {e}")
            return []
    
    def create_dns_record(self, domain: str, record_type: str, name: str, content: str, 
                         ttl: int = 1, proxied: bool = False) -> bool:
        """
        Create a DNS record.
        
        Args:
            domain: Domain name
            record_type: Record type (A, AAAA, CNAME, MX, TXT, etc.)
            name: Record name (e.g., 'www', '@' for root)
            content: Record content (IP address, domain, etc.)
            ttl: Time to live (1 for automatic)
            proxied: Whether to proxy through Cloudflare
            
        Returns:
            True if successful, False otherwise
        """
        zone = self.find_zone(domain)
        if not zone:
            self.log_error(f"Zone not found for domain: {domain}")
            return False
        
        try:
            zone_id = zone.id
            
            # Handle @ for root domain
            if name == '@':
                name = domain
            elif not name.endswith(domain):
                name = f"{name}.{domain}" if name else domain
            
            record_data = {
                'type': record_type.upper(),
                'name': name,
                'content': content,
                'ttl': ttl,
                'proxied': proxied
            }
            
            self.log_info(f"Creating DNS record: {name} ({record_type}) -> {content}")
            result = self.cf.dns.records.create(zone_id=zone_id, **record_data)
            self.log_success(f"DNS record created successfully: {result.id}")
            return True
        except Exception as e:
            self.log_error(f"Failed to create DNS record: {e}")
            return False
    
    def delete_dns_record(self, domain: str, record_name: str, record_type: Optional[str] = None) -> bool:
        """
        Delete a DNS record.
        
        Args:
            domain: Domain name
            record_name: Name of the record to delete
            record_type: Optional record type filter
            
        Returns:
            True if successful, False otherwise
        """
        zone = self.find_zone(domain)
        if not zone:
            self.log_error(f"Zone not found for domain: {domain}")
            return False
        
        try:
            zone_id = zone.id
            records = self.list_dns_records(domain, record_type)
            
            # Find matching record
            target_record = None
            for record in records:
                if record['name'].lower() == record_name.lower() or \
                   record['name'].lower().startswith(f"{record_name}."):
                    target_record = record
                    break
            
            if not target_record:
                self.log_error(f"DNS record not found: {record_name}")
                return False
            
            self.log_info(f"Deleting DNS record: {target_record['name']} ({target_record['type']})")
            self.cf.dns.records.delete(zone_id=zone_id, dns_record_id=target_record['id'])
            self.log_success("DNS record deleted successfully")
            return True
        except Exception as e:
            self.log_error(f"Failed to delete DNS record: {e}")
            return False
    
    def purge_cache(self, domain: str, files: Optional[List[str]] = None) -> bool:
        """
        Purge Cloudflare cache for a domain.
        
        Args:
            domain: Domain name
            files: Optional list of specific files/URLs to purge (None = purge all)
            
        Returns:
            True if successful, False otherwise
        """
        zone = self.find_zone(domain)
        if not zone:
            self.log_error(f"Zone not found for domain: {domain}")
            return False
        
        try:
            zone_id = zone.id
            
            if files:
                self.log_info(f"Purging specific files from cache for {domain}...")
                data = {'files': files}
            else:
                self.log_info(f"Purging all cache for {domain}...")
                data = {'purge_everything': True}
            
            self.cf.cache.purge(zone_id=zone_id, **data)
            self.log_success("Cache purged successfully")
            return True
        except Exception as e:
            self.log_error(f"Failed to purge cache: {e}")
            return False
    
    def get_firewall_rules(self, domain: str) -> List[Dict]:
        """
        Get firewall rules for a domain.
        
        Args:
            domain: Domain name
            
        Returns:
            List of firewall rule dictionaries
        """
        zone = self.find_zone(domain)
        if not zone:
            self.log_error(f"Zone not found for domain: {domain}")
            return []
        
        try:
            zone_id = zone.id
            self.log_info(f"Fetching firewall rules for {domain}...")
            rules_response = self.cf.firewall.rules.list(zone_id=zone_id)
            # Use model_dump() if available (Pydantic v2), fallback to vars()
            rules = [
                rule.model_dump() if hasattr(rule, 'model_dump') else vars(rule)
                for rule in rules_response
            ]
            self.log_success(f"Found {len(rules)} firewall rule(s)")
            return rules
        except Exception as e:
            self.log_error(f"Failed to fetch firewall rules: {e}")
            return []
    
    def enable_development_mode(self, domain: str, enable: bool = True) -> bool:
        """
        Enable or disable development mode for a domain.
        
        Args:
            domain: Domain name
            enable: True to enable, False to disable
            
        Returns:
            True if successful, False otherwise
        """
        zone = self.find_zone(domain)
        if not zone:
            self.log_error(f"Zone not found for domain: {domain}")
            return False
        
        try:
            zone_id = zone.id
            mode = 'on' if enable else 'off'
            self.log_info(f"{'Enabling' if enable else 'Disabling'} development mode for {domain}...")
            
            data = {'value': mode}
            self.cf.zones.settings.development_mode.edit(zone_id=zone_id, **data)
            self.log_success(f"Development mode {'enabled' if enable else 'disabled'}")
            return True
        except Exception as e:
            self.log_error(f"Failed to change development mode: {e}")
            return False
    
    def get_zone_settings(self, domain: str) -> Dict:
        """
        Get all settings for a zone.
        
        Args:
            domain: Domain name
            
        Returns:
            Dictionary of zone settings
        """
        zone = self.find_zone(domain)
        if not zone:
            self.log_error(f"Zone not found for domain: {domain}")
            return {}
        
        try:
            zone_id = zone.id
            self.log_info(f"Fetching zone settings for {domain}...")
            settings_response = self.cf.zones.settings.list(zone_id=zone_id)
            # Efficiently create dictionary in one pass
            settings_dict = {
                s.id: (s.model_dump() if hasattr(s, 'model_dump') else vars(s))
                for s in settings_response
            }
            self.log_success(f"Retrieved {len(settings_dict)} settings")
            return settings_dict
        except Exception as e:
            self.log_error(f"Failed to fetch zone settings: {e}")
            return {}
    
    def execute_command(self, command: str) -> bool:
        """
        Parse and execute a natural language command.
        
        Args:
            command: Natural language command
            
        Returns:
            True if successful, False otherwise
        """
        command_lower = command.lower().strip()
        
        # List zones
        if any(phrase in command_lower for phrase in ['list zones', 'show zones', 'list domains', 'show domains']):
            zones = self.get_zones(force_refresh=True)
            if zones:
                print(f"\n{Fore.CYAN}╔══════════════════════════════════════════╗")
                print(f"║         CLOUDFLARE ZONES                 ║")
                print(f"╚══════════════════════════════════════════╝{Style.RESET_ALL}\n")
                for zone in zones:
                    status = f"{Fore.GREEN}✓{Style.RESET_ALL}" if zone.status == 'active' else f"{Fore.YELLOW}◐{Style.RESET_ALL}"
                    print(f"  {status} {zone.name} (ID: {zone.id})")
            return True
        
        # List DNS records
        match = re.search(r'(?:list|show) (?:dns )?records? (?:for |on )?([a-zA-Z0-9.-]+)', command_lower)
        if match:
            domain = match.group(1)
            records = self.list_dns_records(domain)
            if records:
                print(f"\n{Fore.CYAN}╔══════════════════════════════════════════╗")
                print(f"║         DNS RECORDS FOR {domain.upper():<15}║")
                print(f"╚══════════════════════════════════════════╝{Style.RESET_ALL}\n")
                for record in records:
                    proxy = f"{Fore.YELLOW}☁{Style.RESET_ALL}" if record.get('proxied') else "  "
                    print(f"  {proxy} {record['type']:<6} {record['name']:<30} → {record['content']}")
            return True
        
        # Create DNS record
        match = re.search(r'(?:create|add) (?:dns )?record (?:for |on )?([a-zA-Z0-9.-]+) (?:type |)([A-Z]+) (?:name |)([a-zA-Z0-9.@-]+) (?:content |pointing to |)([a-zA-Z0-9.:/\-]+)', command_lower)
        if match:
            domain, record_type, name, content = match.groups()
            return self.create_dns_record(domain, record_type, name, content)
        
        # Delete DNS record
        match = re.search(r'(?:delete|remove) (?:dns )?record ([a-zA-Z0-9.-]+) (?:from |on )?([a-zA-Z0-9.-]+)', command_lower)
        if match:
            record_name, domain = match.groups()
            return self.delete_dns_record(domain, record_name)
        
        # Purge cache
        match = re.search(r'(?:purge|clear) (?:cache|cdn) (?:for |on )?([a-zA-Z0-9.-]+)', command_lower)
        if match:
            domain = match.group(1)
            return self.purge_cache(domain)
        
        # Enable/disable dev mode
        match = re.search(r'(enable|disable) dev(?:elopment)? mode (?:for |on )?([a-zA-Z0-9.-]+)', command_lower)
        if match:
            action, domain = match.groups()
            return self.enable_development_mode(domain, enable=(action == 'enable'))
        
        # Get zone settings
        match = re.search(r'(?:show|get) settings (?:for |on )?([a-zA-Z0-9.-]+)', command_lower)
        if match:
            domain = match.group(1)
            settings = self.get_zone_settings(domain)
            if settings:
                print(f"\n{Fore.CYAN}╔══════════════════════════════════════════╗")
                print(f"║         SETTINGS FOR {domain.upper():<18}║")
                print(f"╚══════════════════════════════════════════╝{Style.RESET_ALL}\n")
                for key, setting in settings.items():
                    print(f"  {key:<30} : {setting.get('value', 'N/A')}")
            return True
        
        # List firewall rules
        match = re.search(r'(?:list|show) firewall (?:rules? )?(?:for |on )?([a-zA-Z0-9.-]+)', command_lower)
        if match:
            domain = match.group(1)
            rules = self.get_firewall_rules(domain)
            if rules:
                print(f"\n{Fore.CYAN}╔══════════════════════════════════════════╗")
                print(f"║         FIREWALL RULES FOR {domain.upper():<13}║")
                print(f"╚══════════════════════════════════════════╝{Style.RESET_ALL}\n")
                for rule in rules:
                    action = rule.get('action', 'unknown')
                    description = rule.get('description', 'No description')
                    print(f"  {action.upper():<10} {description}")
            return True
        
        self.log_warning(f"Command not recognized: {command}")
        self.log_info("Try commands like:")
        print("  - list zones")
        print("  - list dns records for example.com")
        print("  - create dns record for example.com type A name www content 1.2.3.4")
        print("  - delete dns record www from example.com")
        print("  - purge cache for example.com")
        print("  - enable dev mode for example.com")
        print("  - show settings for example.com")
        return False


def main():
    """Main function for testing"""
    print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║      MR. MATRIX CLOUDFLARE AUTOMATED AGENT                  ║
║      =====================================                   ║
║                                                              ║
║      Your automated assistant for Cloudflare tasks          ║
║      Just tell me what to do, and I'll handle it!           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """)
    
    try:
        agent = CloudflareAgent()
        agent.log_success("Agent initialized successfully!")
        
        # Example command
        agent.log_info("Example: 'list zones' or 'show dns records for example.com'")
        
    except Exception as e:
        print(f"{Fore.RED}Failed to initialize agent: {e}{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Please set CLOUDFLARE_API_TOKEN environment variable or create a config file.{Style.RESET_ALL}")


if __name__ == '__main__':
    main()
