---
name: Bug report
about: Create a report to help us improve

---

### Describe the bug

A clear and concise description of what the bug is.

### Reproduction Script

Provide a script to reproduce the error using the following template, 
replacing `<YOUR SCRIPT>` with your script:

```python
import sys
import pkg_resources
import platform
print(platform.platform())
print(sys.version_info)
print(pkg_resources.get_distribution("nes-py").version)
print(pkg_resources.get_distribution("gym-super-mario-bros").version)
<YOUR SCRIPT>
```

### Expected behavior

A clear and concise description of what you expected to happen.

### Screenshots

If applicable, add screenshots to help explain your problem.

### Additional context

Add any other context about the problem here.
