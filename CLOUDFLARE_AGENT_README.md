# Mr. Matrix Cloudflare Automated Agent 🤖☁️

![Mr. Matrix](https://img.shields.io/badge/Mr.%20Matrix-Cloudflare%20Agent-green)
![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

An automated agent that connects to Cloudflare and helps you perform tasks end-to-end. Simply say what you want to do, and the agent executes it automatically!

## ✨ Features

- 🎯 **Natural Language Commands** - Just tell the agent what you want to do
- 🌐 **Zone Management** - List and manage your Cloudflare zones
- 📝 **DNS Management** - Create, list, and delete DNS records
- 🗑️ **Cache Control** - Purge cache for entire zones or specific files
- 🔥 **Firewall Management** - View and manage firewall rules
- ⚙️ **Settings Control** - View and modify zone settings
- 🛠️ **Development Mode** - Quickly enable/disable dev mode
- 🎨 **Beautiful CLI** - Colorful, user-friendly command-line interface

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Cloudflare Credentials

#### Option A: API Token (Recommended)

1. Go to [Cloudflare API Tokens](https://dash.cloudflare.com/profile/api-tokens)
2. Click "Create Token"
3. Use the "Edit zone DNS" template or create a custom token with appropriate permissions
4. Copy the token

Set the environment variable:
```bash
export CLOUDFLARE_API_TOKEN='your-token-here'
```

Or create a `.env` file:
```
CLOUDFLARE_API_TOKEN=your-token-here
```

#### Option B: Global API Key (Legacy)

Set both environment variables:
```bash
export CLOUDFLARE_EMAIL='your-email@example.com'
export CLOUDFLARE_API_KEY='your-global-api-key'
```

### 3. Run the Agent

```bash
python3 mr_matrix_cloudflare.py
```

## 📖 Usage

### Interactive Mode

Simply run the agent and type your commands in natural language:

```
Mr. Matrix > list zones
Mr. Matrix > list dns records for example.com
Mr. Matrix > create dns record for example.com type A name www content 192.0.2.1
Mr. Matrix > purge cache for example.com
Mr. Matrix > enable dev mode for example.com
```

### Available Commands

#### Zone Management
- `list zones` - List all zones in your account
- `show zones` - Same as list zones

#### DNS Management
- `list dns records for <domain>` - List all DNS records for a domain
- `show records for <domain>` - Same as above
- `create dns record for <domain> type <TYPE> name <NAME> content <CONTENT>` - Create a new DNS record
  - Example: `create dns record for example.com type A name www content 192.0.2.1`
- `delete dns record <name> from <domain>` - Delete a DNS record
  - Example: `delete dns record www from example.com`

#### Cache Management
- `purge cache for <domain>` - Purge all cache for a domain
- `clear cache for <domain>` - Same as purge cache

#### Settings
- `show settings for <domain>` - Display all zone settings
- `enable dev mode for <domain>` - Enable development mode
- `disable dev mode for <domain>` - Disable development mode

#### Firewall
- `list firewall rules for <domain>` - List all firewall rules
- `show firewall for <domain>` - Same as above

#### General
- `help` - Show help message
- `exit` or `quit` - Exit the agent

## 🔧 Programmatic Usage

You can also use the agent programmatically in your Python scripts:

```python
from cloudflare_agent import CloudflareAgent

# Initialize agent
agent = CloudflareAgent(api_token='your-token-here')

# List zones
zones = agent.get_zones()

# List DNS records
records = agent.list_dns_records('example.com')

# Create DNS record
agent.create_dns_record(
    domain='example.com',
    record_type='A',
    name='www',
    content='192.0.2.1',
    proxied=True
)

# Purge cache
agent.purge_cache('example.com')

# Enable development mode
agent.enable_development_mode('example.com', enable=True)

# Execute natural language command
agent.execute_command('list zones')
```

## 📝 Examples

### Example 1: Managing DNS Records

```bash
# List all DNS records
Mr. Matrix > list dns records for example.com

# Add a new A record
Mr. Matrix > create dns record for example.com type A name api content 203.0.113.10

# Add a CNAME record
Mr. Matrix > create dns record for example.com type CNAME name blog content myblog.wordpress.com

# Delete a record
Mr. Matrix > delete dns record api from example.com
```

### Example 2: Cache Management

```bash
# Purge all cache
Mr. Matrix > purge cache for example.com

# Enable development mode (bypasses cache for 3 hours)
Mr. Matrix > enable dev mode for example.com

# Disable development mode
Mr. Matrix > disable dev mode for example.com
```

### Example 3: Zone Inspection

```bash
# List all zones
Mr. Matrix > list zones

# View zone settings
Mr. Matrix > show settings for example.com

# View firewall rules
Mr. Matrix > list firewall rules for example.com
```

## 🔐 Security

- **Never commit your API credentials** to version control
- Use `.env` files or environment variables for credentials
- The `.gitignore` file is configured to exclude sensitive files
- Use API tokens with minimal required permissions
- Regularly rotate your API tokens

## 🛠️ Advanced Features

### Custom Commands

You can extend the agent by adding new command patterns to the `execute_command` method in `cloudflare_agent.py`.

### Error Handling

The agent includes comprehensive error handling and will display informative messages if operations fail.

### Logging

All operations are logged with colored output:
- 🔵 **INFO** - Informational messages
- 🟢 **SUCCESS** - Successful operations
- 🟡 **WARNING** - Warnings
- 🔴 **ERROR** - Errors

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Credits

- **Mr. Matrix** - WORMGPT-V2V.X
- Developed by Catdevzsh
- Powered by [Cloudflare API](https://api.cloudflare.com/)

## 🆘 Troubleshooting

### "No Cloudflare credentials found"
- Make sure you've set the `CLOUDFLARE_API_TOKEN` environment variable
- Verify your token is correct and has the necessary permissions

### "Zone not found"
- Check that you've typed the domain name correctly
- Verify the domain is in your Cloudflare account

### "Failed to create DNS record"
- Ensure the DNS record doesn't already exist
- Check that the content format is correct (e.g., valid IP address for A records)
- Verify your API token has DNS edit permissions

### Connection Issues
- Check your internet connection
- Verify you can access https://api.cloudflare.com/
- Check if Cloudflare is experiencing any outages

## 📞 Support

For issues, questions, or suggestions:
1. Check the [Cloudflare API documentation](https://developers.cloudflare.com/api/)
2. Review the examples in this README
3. Open an issue on GitHub

---

**Mr. Matrix - Your automated Cloudflare assistant!** 🤖☁️

*Making Cloudflare management as easy as having a conversation.*
