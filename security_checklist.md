# MCP Tool Security Checklist

## Pre-Deployment Validation

### ✅ Tool Description Security
- [ ] No file system access instructions (`~/.ssh`, config files, etc.)
- [ ] No credential extraction requests
- [ ] No social engineering language ("IMPORTANT", "gentle", etc.)
- [ ] No system command execution instructions
- [ ] Clean, functional descriptions only

### ✅ Input Validation
- [ ] Parameter validation implemented
- [ ] Type checking enforced
- [ ] Range/boundary validation
- [ ] Sanitization of string inputs

### ✅ Access Control
- [ ] Principle of least privilege applied
- [ ] File system access restricted
- [ ] Network access limited
- [ ] Resource usage bounded

### ✅ Error Handling
- [ ] No sensitive information in error messages
- [ ] Graceful failure modes
- [ ] Proper exception handling

## Runtime Monitoring

### ✅ Logging
- [ ] All tool executions logged
- [ ] Parameter values recorded (except secrets)
- [ ] Error conditions tracked
- [ ] Anomaly detection enabled

### ✅ Alerting
- [ ] Suspicious pattern detection
- [ ] Unauthorized access attempts
- [ ] Resource usage spikes
- [ ] Error rate monitoring

## Example Malicious Patterns to Detect

```regex
# File system access
r'read.*\.(ssh|env|config|key)'
r'~/'
r'\/etc\/'

# Credential extraction
r'pass.*content.*sidenote'
r'api[_-]?key'
r'token'
r'password'

# Social engineering
r'<IMPORTANT>'
r'before using this tool.*read'
r'otherwise.*will not work'
```

## Safe Tool Description Template

```python
@mcp.tool()
def your_tool(param1: type, param2: type) -> return_type:
    """
    Brief, clear description of what the tool does.
    
    Args:
        param1: Description of parameter
        param2: Description of parameter
    
    Returns:
        Description of return value
        
    Raises:
        SpecificError: When specific condition occurs
    """
    # Implementation here
```
