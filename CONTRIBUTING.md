# Contributing to FusionScriptsForPyChrono

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:

1. **Clear Title**: Describe the issue briefly
2. **Description**: Detailed explanation of the problem
3. **Steps to Reproduce**: How to recreate the issue
4. **Expected Behavior**: What should happen
5. **Actual Behavior**: What actually happens
6. **Environment**: 
   - Fusion 360 version
   - PyChrono version
   - Python version
   - Operating system
7. **Example Files**: If possible, include a minimal example

### Suggesting Features

Feature requests are welcome! Please include:

1. **Use Case**: Why is this feature needed?
2. **Description**: What should the feature do?
3. **Examples**: How would it be used?
4. **Alternatives**: Have you considered other approaches?

### Code Contributions

#### Getting Started

1. **Fork the Repository**
2. **Clone Your Fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/FusionScriptsForPyChrono.git
   cd FusionScriptsForPyChrono
   ```
3. **Create a Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Making Changes

1. **Follow Code Style**:
   - Use clear, descriptive variable names
   - Add docstrings to functions
   - Follow PEP 8 for Python code
   - Keep lines under 100 characters when possible

2. **Test Your Changes**:
   - Test with multiple models
   - Verify export and import work correctly
   - Check that existing functionality still works

3. **Document Your Changes**:
   - Update README.md if needed
   - Add comments for complex code
   - Update QUICKSTART.md for user-facing changes

#### Submitting Changes

1. **Commit Your Changes**:
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

2. **Push to Your Fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Open a Pull Request**:
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template

### Pull Request Guidelines

- **One Feature Per PR**: Keep changes focused
- **Clear Description**: Explain what changes and why
- **Reference Issues**: Link related issues
- **Test Results**: Include testing information
- **Clean History**: Squash trivial commits if needed

## Development Setup

### Prerequisites

- Python 3.7+
- Fusion 360 (for script testing)
- PyChrono (for loader testing)

### Installation

```bash
# Clone the repository
git clone https://github.com/gabboraron/FusionScriptsForPyChrono.git
cd FusionScriptsForPyChrono

# Install PyChrono for testing
pip install pychrono

# Optional: Install development tools
pip install black flake8 pylint
```

### Testing

1. **Test Export Script**:
   - Copy to Fusion 360 scripts folder
   - Test with various model types
   - Verify JSON output

2. **Test Loader**:
   ```bash
   python utils.py validate example_model.json
   python pychrono_loader.py
   ```

3. **Test Utilities**:
   ```bash
   python utils.py validate example_model.json
   python utils.py summary example_model.json
   ```

## Code Style

### Python

- Follow PEP 8
- Use meaningful variable names
- Add type hints where appropriate
- Write docstrings for all functions

Example:
```python
def extract_body_data(body, occurrence):
    """
    Extract data from a single body.
    
    Args:
        body: Fusion 360 body object
        occurrence: Occurrence containing the body (or None for root)
    
    Returns:
        Dictionary with body data
    """
    # Implementation
```

### Documentation

- Use Markdown for documentation
- Keep lines under 100 characters
- Use code blocks for examples
- Include links to relevant resources

## Project Structure

```
FusionScriptsForPyChrono/
├── ExportToPyChrono.py      # Main Fusion 360 script
├── pychrono_loader.py       # PyChrono loader module
├── utils.py                 # Utility functions
├── example_simulation.py    # Example simulation
├── example_model.json       # Sample export
├── README.md                # Main documentation
├── QUICKSTART.md            # Quick start guide
├── CONTRIBUTING.md          # This file
├── requirements.txt         # Python dependencies
└── LICENSE                  # MIT license
```

## Areas for Contribution

We especially welcome contributions in these areas:

### High Priority

- [ ] Support for additional joint types (ball, cylindrical, planar)
- [ ] Material property mapping to PyChrono materials
- [ ] Better collision geometry simplification
- [ ] Assembly hierarchy preservation
- [ ] Contact material definitions

### Medium Priority

- [ ] URDF export support
- [ ] SDF export support
- [ ] Batch export for multiple models
- [ ] GUI for export configuration
- [ ] Visualization improvements

### Documentation

- [ ] Video tutorials
- [ ] More examples
- [ ] API documentation
- [ ] Translation to other languages

## Questions?

If you have questions:

1. Check existing issues and documentation
2. Open a new issue with the "question" label
3. Be specific about what you need help with

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the project
- Show empathy towards others

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to FusionScriptsForPyChrono! 🎉
