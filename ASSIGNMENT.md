# 🏗️ Part 1: Monorepo Setup

## Convert to Unified Monorepo Management

Transform the current project structure into a unified monorepo that eliminates code duplication and dependency conflicts while preserving the ability to develop, test, and deploy each service independently.

**Things to note about the services:**

- **data-processor**: [FastAPI](https://fastapi.tiangolo.com/) service handling data transformation, filtering, and aggregation with endpoints for processing medical data
- **model-service**: ML inference service providing model training and prediction capabilities using [scikit-learn](https://scikit-learn.org/)
- Both services are stateless, designed for frequent updates, and share common validation and logging utilities
- The applications should remain independently deployable while benefiting from shared infrastructure and tooling
- Both services must continue to function correctly after the conversion

Choose a monorepo management solution and justify your selection based on the specific needs of this Python-based, microservices architecture.

### Checklist (Choose & Justify)

Choose and justify your design choices:

- [ ] **Monorepo tool selection**: Choose your preferred tool ([Pants](https://www.pantsbuild.org/), [Poetry workspaces](https://python-poetry.org/docs/managing-dependencies/#dependency-groups), [Bazel](https://bazel.build/), etc.) and explain why it fits this use case better than alternatives
- [ ] **Dependency resolution**: Unify the conflicting dependencies into a single, coherent set that works for both services
- [ ] **Shared code organization**: Restructure the duplicated `utils/` code into a proper shared library accessible by both services
- [ ] **Build orchestration**: Set up efficient build, test, lint, and format tasks that work on individual projects or the entire monorepo
- [ ] **Development workflow**: Ensure both services can still be developed, tested, and run independently during development
- [ ] **Configuration management**: Centralize tooling configuration (linting, formatting, testing) with project-specific overrides where needed

### Acceptance Criteria

- ✅ Both services run successfully after monorepo conversion with unified dependencies
- ✅ Shared `utils/` code is properly organized and eliminates duplication
- ✅ Single command can install all dependencies and set up the development environment
- ✅ Individual services can be tested, linted, and run independently
- ✅ Monorepo-wide operations (test all, lint all, format all) work efficiently
- ✅ `SOLUTION.md` explains **why** you chose your specific approach and tools

# 🚀 Part 2: CI/CD Pipeline

## Design Efficient Build and Deployment Pipeline

Create a CI/CD pipeline that leverages the monorepo structure and integrates with your chosen monorepo tool from Part 1 to deliver fast, reliable automation with emphasis on build efficiency and developer experience.

**⚡ Focus on efficiency:**
- **🚀 Minimize startup overhead**: Avoid redundant setup across pipeline steps
- **💾 Leverage caching**: Build caches, dependency caches, test result caches
- **🔄 Incremental builds**: Only test/build what has actually changed
- **⚡ Parallel execution**: Run independent operations concurrently
- **⚠️ Fast feedback**: Quick failure detection and clear error reporting

### Pipeline Requirements

Design a CI/CD workflow that includes:

- **Environment setup**: Efficient installation of unified dependencies
- **Code quality gates**: Linting and formatting validation across all code
- **Testing strategy**: Run tests for affected services with option to test everything
- **Pre-commit integration**: Local validation hooks that catch issues before commit
- **Local CI simulation**: Pipeline must be testable locally (e.g., using [act](https://github.com/nektos/act) for GitHub Actions or equivalent tools)
- **CI runner optimization**: Create optimized CI runner images with pre-installed dependencies and tooling to avoid repetitive installation steps in every pipeline run
- **Deployment readiness**: Show how services would be built/packaged for deployment

### Checklist (Choose & Justify)

Choose and justify your CI/CD implementation:

- [ ] **Platform choice**: Select CI/CD platform ([GitHub Actions](https://docs.github.com/en/actions), [GitLab CI](https://docs.gitlab.com/ee/ci/), local scripts, etc.) and justify why it fits the requirements
- [ ] **Build optimization strategy**: Implement specific techniques to minimize build time and resource usage
- [ ] **Change detection logic**: Show how the pipeline determines which projects need building/testing
- [ ] **Caching implementation**: Use appropriate caching for dependencies, build outputs, or test results
- [ ] **CI runner optimization**: Build custom CI runner images with pre-installed dependencies and tooling to eliminate setup overhead in every pipeline execution
- [ ] **Pre-commit setup**: Configure [pre-commit hooks](https://pre-commit.com/) that run quickly and catch common issues early
- [ ] **Local CI testing**: Provide commands to run the full CI pipeline locally for testing and debugging
- [ ] **Performance measurement**: Demonstrate efficiency gains compared to building projects separately

### Acceptance Criteria

- ✅ Complete CI/CD pipeline runs successfully on the monorepo structure
- ✅ Pipeline demonstrates measurable performance improvements over separate builds
- ✅ Pre-commit hooks are configured and functional
- ✅ Pipeline can be executed and tested locally with provided commands/tools
- ✅ CI runner images are optimized with pre-built dependencies to minimize pipeline execution time
- ✅ Caching and incremental builds work as intended
- ✅ Pipeline configuration can be easily understood and modified
- ✅ `SOLUTION.md` explains optimization strategies and quantifies expected benefits for a development team
