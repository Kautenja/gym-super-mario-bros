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

Please also include:

- the exact install command(s) you ran
- whether this is a `pip`, `venv`, `conda`, or system Python environment
- for Linux loader errors, the active `libstdc++` version if you know it
- for Windows build errors, whether MSVC / Visual Studio Build Tools are installed

### Expected behavior

A clear and concise description of what you expected to happen.

### Screenshots

If applicable, add screenshots to help explain your problem.

### Additional context

Add any other context about the problem here.
