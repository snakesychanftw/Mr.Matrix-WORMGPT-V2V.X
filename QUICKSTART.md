# Quick Start Guide - Mr. Matrix Cloudflare Automated Agent

## 🚀 Get Started in 3 Minutes

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `cloudflare` - Official Cloudflare Python SDK
- `colorama` - For beautiful colored output
- `python-dotenv` - For environment variable management

### Step 2: Get Your Cloudflare API Token

1. Visit [https://dash.cloudflare.com/profile/api-tokens](https://dash.cloudflare.com/profile/api-tokens)
2. Click **"Create Token"**
3. Use the **"Edit zone DNS"** template OR create a custom token with these permissions:
   - Zone - Zone - Read
   - Zone - DNS - Edit
   - Zone - Cache Purge - Purge
   - Zone - Zone Settings - Edit
   
4. Copy your token (you'll only see it once!)

### Step 3: Set Your API Token

**Option A: Environment Variable (Recommended)**
```bash
export CLOUDFLARE_API_TOKEN='your_token_here'
```

**Option B: Create a .env file**
```bash
echo "CLOUDFLARE_API_TOKEN=your_token_here" > .env
```

### Step 4: Run the Agent!

```bash
python3 mr_matrix_cloudflare.py
```

## 📝 Your First Commands

Once the agent is running, try these commands:

```
Mr. Matrix > list zones
Mr. Matrix > list dns records for example.com
Mr. Matrix > help
```

## 🎯 Common Tasks

### View All Your Domains
```
list zones
```

### Manage DNS Records
```
# View records
list dns records for example.com

# Add a new A record
create dns record for example.com type A name api content 192.0.2.1

# Add a CNAME record  
create dns record for example.com type CNAME name www content example.com

# Delete a record
delete dns record api from example.com
```

### Cache Management
```
# Clear all cache
purge cache for example.com

# Enable development mode (bypasses cache for 3 hours)
enable dev mode for example.com

# Disable development mode
disable dev mode for example.com
```

### View Settings
```
# See all zone settings
show settings for example.com

# View firewall rules
list firewall rules for example.com
```

## 🔍 Troubleshooting

### "No Cloudflare credentials found"
- Make sure you've set the `CLOUDFLARE_API_TOKEN` environment variable
- Or create a `.env` file with your token

### "Zone not found"
- Check that you typed the domain name correctly
- Verify the domain is in your Cloudflare account

### "Permission denied" errors
- Your API token needs the appropriate permissions
- Create a new token with the required scopes

### Import errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

## 📖 Learn More

- Full documentation: [CLOUDFLARE_AGENT_README.md](CLOUDFLARE_AGENT_README.md)
- Example scripts: [example_usage.py](example_usage.py)
- Cloudflare API Docs: [https://developers.cloudflare.com/api/](https://developers.cloudflare.com/api/)

## 🎓 Advanced Usage

### Programmatic Use

```python
from cloudflare_agent import CloudflareAgent

# Initialize
agent = CloudflareAgent()

# List zones
zones = agent.get_zones()

# Create DNS record
agent.create_dns_record('example.com', 'A', 'api', '192.0.2.1')

# Natural language commands
agent.execute_command('purge cache for example.com')
```

### Batch Operations

Create a script to perform multiple operations:

```python
from cloudflare_agent import CloudflareAgent

agent = CloudflareAgent()

# Add multiple DNS records
records = [
    ('A', 'api', '192.0.2.1'),
    ('A', 'app', '192.0.2.2'),
    ('CNAME', 'www', 'example.com'),
]

for rec_type, name, content in records:
    agent.create_dns_record('example.com', rec_type, name, content)
```

## 🆘 Need Help?

- Type `help` in the agent for available commands
- Check the logs for detailed error messages
- Visit Cloudflare's API documentation

---

**Happy automating with Mr. Matrix! 🤖☁️**
