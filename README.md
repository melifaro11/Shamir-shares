# Shamir's Secret Sharing

Python implementation of Shamir's Secret Sharing: https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing

## Usage

### Import library
```python
from secret_sharing import ShamirSharing
```

### Create share

```python
shamir = ShamirSharing()
keys = s.split_secret('Hallo world', 2, 4)
```

### Recover share

```python
shamir.recover_secret([keys[0], keys[2]]))
```