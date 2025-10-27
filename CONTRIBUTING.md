# Contributing to Tech Watch Scraper

Thank you for your interest in contributing! This document provides guidelines and standards for contributing to this project.

## Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd tech-watch-scraper
```

2. Install dependencies using UV:
```bash
uv sync --all-groups
```

3. Install pre-commit hooks:
```bash
uv run pre-commit install --hook-type commit-msg --hook-type pre-commit
```

## Code Quality Standards

### Ruff Configuration

This project uses Ruff for linting and formatting with the following standards:
- Line length: 88 characters
- Target version: Python 3.12
- Selected rules: E (pycodestyle errors), F (pyflakes), I (isort), UP (pyupgrade)
- Quote style: double quotes

### Running Code Quality Checks

Run linting and formatting checks locally:
```bash
./scripts/lint.sh
```

Run with auto-fix:
```bash
./scripts/lint.sh --fix
```

## Conventional Commits

This project uses [Conventional Commits](https://www.conventionalcommits.org/) for commit messages. The format ensures clear, structured commit history and enables automated versioning.

### Commit Message Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Commit Types

- **feat**: A new feature (triggers minor version bump)
- **fix**: A bug fix (triggers patch version bump)
- **docs**: Documentation only changes
- **style**: Changes that don't affect code meaning (formatting, white-space)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Performance improvement
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes affecting build system or dependencies
- **ci**: Changes to CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files

### Breaking Changes

Add `!` after the type or add `BREAKING CHANGE:` in the footer to trigger a major version bump:

```
feat!: change API response format

BREAKING CHANGE: API now returns data in different structure
```

### Examples

Good commit messages:
```
feat(scraper): add support for RSS feed scraping
fix(formatter): handle missing video descriptions correctly
docs: update README with new configuration options
refactor(config): simplify API key validation
test(scraper): add unit tests for rate limiting
```

Bad commit messages:
```
updated stuff
fix bug
WIP
asdfasdf
```

### Commitizen Helper

The pre-commit hook will validate your commit messages. You can also use commitizen interactively:

```bash
git add .
uv run cz commit
```

This will guide you through creating a properly formatted commit message.

## Feature Branch Workflow

### Creating a Feature Branch

Use the helper script:
```bash
./scripts/new-feature.sh my-feature-name
```

Or manually:
```bash
git checkout -b feature/my-feature-name
```

### Branch Naming Convention

- Features: `feature/description`
- Bug fixes: `fix/description`
- Documentation: `docs/description`
- Refactoring: `refactor/description`

### Development Workflow

1. Create a feature branch
2. Make your changes
3. Run code quality checks: `./scripts/lint.sh`
4. Commit using conventional commits
5. Push your branch: `git push -u origin feature/my-feature-name`
6. Create a pull request on GitHub

## Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality:

### Pre-commit Hook (runs before commit)
- Ruff linting with auto-fix
- Ruff formatting

### Commit-msg Hook (runs on commit message)
- Validates conventional commit format

If the hooks fail, fix the issues and try committing again. The hooks will automatically fix most formatting issues.

### Bypassing Hooks (Not Recommended)

In rare cases where you need to bypass hooks:
```bash
git commit --no-verify
```

**Warning**: This should only be used in exceptional circumstances, as it bypasses code quality checks.

## Pull Requests

### Before Creating a PR

1. Ensure all tests pass
2. Run code quality checks: `./scripts/lint.sh`
3. Update documentation if needed
4. Ensure commits follow conventional commit format

### PR Guidelines

- Provide a clear description of the changes
- Reference any related issues
- Ensure CI checks pass
- Request review from maintainers
- Keep PRs focused and reasonably sized

### PR Title Format

PR titles should also follow conventional commit format:
```
feat: add new scraping source
fix: resolve rate limiting issue
```

## Version Management

### Automatic Versioning

Version bumps are automated based on conventional commits:
- `feat`: minor version bump (0.1.0 → 0.2.0)
- `fix`: patch version bump (0.1.0 → 0.1.1)
- `BREAKING CHANGE`: major version bump (0.1.0 → 1.0.0)

### Manual Version Bump

Use the helper script:
```bash
./scripts/bump.sh          # Automatic based on commits
./scripts/bump.sh patch    # Force patch bump
./scripts/bump.sh minor    # Force minor bump
./scripts/bump.sh major    # Force major bump
```

## CI/CD Pipeline

### Continuous Integration

On every pull request and push to main:
- Ruff linting check
- Ruff formatting check

### Release Workflow

On push to main:
- Automatic version bump (if needed)
- CHANGELOG.md generation/update
- Git tag creation
- GitHub release creation

## Getting Help

If you have questions or need help:
- Check existing issues on GitHub
- Review this documentation
- Open a new issue with the `question` label

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help create a welcoming environment for all contributors
