# Contributing to Cyber Tonic

Thank you for your interest in contributing to Cyber Tonic! This guide will help you get started with contributing to the project.

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Development Setup](#development-setup)
3. [Coding Standards](#coding-standards)
4. [Testing](#testing)
5. [Submitting Changes](#submitting-changes)
6. [Code Review Process](#code-review-process)

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- Git
- Basic knowledge of Streamlit, Python, and cybersecurity concepts

### Fork and Clone
1. **Fork the Repository**: Click "Fork" on the GitHub repository page
2. **Clone Your Fork**: 
   ```bash
   git clone https://github.com/YOUR_USERNAME/cyber_tonic.git
   cd cyber_tonic
   ```
3. **Add Upstream Remote**:
   ```bash
   git remote add upstream https://github.com/mimimakingthings/cyber_tonic.git
   ```

## 🛠️ Development Setup

### Environment Setup
1. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Install Pre-commit Hooks**:
   ```bash
   pre-commit install
   ```

### Development Tools
- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **pytest**: Testing framework
- **pre-commit**: Git hooks for quality checks

## 📝 Coding Standards

### Python Style Guide
We follow **PEP 8** with the following specific guidelines:

#### Code Formatting
- **Line Length**: Maximum 88 characters (Black default)
- **Indentation**: 4 spaces (no tabs)
- **String Quotes**: Use double quotes for strings
- **Import Sorting**: Use isort for consistent import organization

#### Naming Conventions
- **Variables**: `snake_case`
- **Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private Methods**: `_leading_underscore`

#### Documentation
- **Docstrings**: Use Google style docstrings
- **Comments**: Explain why, not what
- **Type Hints**: Use type hints for function parameters and returns

#### Example Code Style
```python
def calculate_maturity_score(
    assessment_data: Dict[str, Any], 
    weights: Optional[Dict[str, float]] = None
) -> float:
    """
    Calculate the overall maturity score for an assessment.
    
    Args:
        assessment_data: Dictionary containing assessment scores
        weights: Optional weights for different functions
        
    Returns:
        Calculated maturity score as a float
        
    Raises:
        ValueError: If assessment_data is empty or invalid
    """
    if not assessment_data:
        raise ValueError("Assessment data cannot be empty")
    
    # Implementation here
    return score
```

### Streamlit Best Practices
- **Session State**: Use `st.session_state` for persistent data
- **Caching**: Use `@st.cache_data` for expensive operations
- **Error Handling**: Provide user-friendly error messages
- **UI Components**: Use consistent styling and layout

### File Organization
- **Apps**: Place Streamlit applications in `apps/`
- **Core Modules**: Place reusable code in `src/`
- **Tests**: Place tests in `tests/` with matching structure
- **Documentation**: Update relevant docs in `docs/`

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_assessment_enhancements.py

# Run with verbose output
pytest -v
```

### Writing Tests
- **Test Structure**: Follow pytest conventions
- **Test Names**: Use descriptive names that explain what is being tested
- **Test Data**: Use fixtures for common test data
- **Mocking**: Mock external dependencies and file operations

#### Example Test
```python
import pytest
from src.assessment_enhancements import calculate_maturity_score

def test_calculate_maturity_score_with_valid_data():
    """Test maturity score calculation with valid assessment data."""
    assessment_data = {
        "GV.OC-1": 8,
        "GV.OC-2": 6,
        "ID.AM-1": 7
    }
    
    result = calculate_maturity_score(assessment_data)
    
    assert isinstance(result, float)
    assert 0 <= result <= 10

def test_calculate_maturity_score_with_empty_data():
    """Test maturity score calculation raises error with empty data."""
    with pytest.raises(ValueError, match="Assessment data cannot be empty"):
        calculate_maturity_score({})
```

### Test Coverage
- **Minimum Coverage**: Aim for 80% test coverage
- **Critical Paths**: Ensure all critical functionality is tested
- **Edge Cases**: Test boundary conditions and error cases
- **Integration Tests**: Test component interactions

## 📤 Submitting Changes

### Workflow
1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**: Follow coding standards and write tests

3. **Run Quality Checks**:
   ```bash
   # Format code
   black src/ tests/
   isort src/ tests/
   
   # Run linting
   flake8 src/ tests/
   
   # Run tests
   pytest
   ```

4. **Commit Changes**:
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

5. **Push and Create PR**:
   ```bash
   git push origin feature/your-feature-name
   # Create Pull Request on GitHub
   ```

### Commit Message Format
We use conventional commits format:

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

Examples:
```
feat: add ISO 27001 standard support
fix: resolve data persistence issue in client portal
docs: update user guide with new features
test: add tests for assessment scoring
```

### Pull Request Guidelines
- **Clear Title**: Describe what the PR does
- **Detailed Description**: Explain the changes and why they're needed
- **Link Issues**: Reference related issues
- **Screenshots**: Include screenshots for UI changes
- **Testing**: Describe how the changes were tested

## 🔍 Code Review Process

### Review Criteria
- **Functionality**: Does the code work as intended?
- **Code Quality**: Follows coding standards and best practices
- **Testing**: Adequate test coverage and quality
- **Documentation**: Updated documentation where needed
- **Performance**: No significant performance regressions

### Review Process
1. **Automated Checks**: All CI checks must pass
2. **Peer Review**: At least one maintainer review required
3. **Feedback**: Address all review comments
4. **Approval**: Maintainer approval required for merge

### Common Review Comments
- **Code Style**: Formatting, naming, or structure issues
- **Testing**: Missing or inadequate tests
- **Documentation**: Missing or unclear documentation
- **Performance**: Potential performance issues
- **Security**: Security considerations

## 🎯 Areas for Contribution

### High Priority
- **New Standards**: Add support for ISO 27001, CMMC 2.0, GDPR
- **Authentication**: Implement user authentication and authorization
- **API Development**: Create REST API for external integrations
- **Testing**: Improve test coverage and add integration tests

### Medium Priority
- **UI/UX Improvements**: Enhance user interface and experience
- **Performance**: Optimize data loading and visualization
- **Documentation**: Improve and expand documentation
- **Accessibility**: Enhance WCAG compliance

### Low Priority
- **Code Refactoring**: Improve code organization and structure
- **Dependencies**: Update and maintain dependencies
- **Examples**: Add more example data and use cases
- **Internationalization**: Add multi-language support

## 📞 Getting Help

### Communication Channels
- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Pull Requests**: For code review and collaboration

### Resources
- **Documentation**: Check `docs/` directory
- **Code Examples**: Review existing code in `src/` and `apps/`
- **Standards**: Refer to NIST CSF 2.0 and other cybersecurity frameworks

## 🙏 Recognition

Contributors will be recognized in:
- **CONTRIBUTORS.md**: List of all contributors
- **Release Notes**: Credit for significant contributions
- **Documentation**: Attribution for documentation contributions

Thank you for contributing to Cyber Tonic! Your efforts help make cybersecurity compliance more accessible and effective for consultants worldwide.

---

**Happy Contributing! 🛡️**
