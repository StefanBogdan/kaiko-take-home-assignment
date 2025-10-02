# Platform Engineer - CI/CD Technical Assignment

As a platform engineer at Kaiko, you'll work with cutting-edge CI/CD technologies to support our AI/ML workloads for healthcare applications. This assignment evaluates your hands-on expertise in monorepo management, build optimization, and implementing efficient CI/CD pipelines.

Please note that while the time needed to complete this technical assignment is flexible and can be adapted to your schedule, we expect it to be completed within a maximum of one standard work week. This ensures the assessment remains focused and relevant, while also giving you the flexibility to manage your time effectively.

## High-Level Overview

- **🏗️ Part 1: Monorepo Setup**  
  Convert the existing separate Python projects into a unified monorepo with shared dependencies and tooling. Eliminate code duplication and resolve dependency conflicts while maintaining independent deployability.

- **🚀 Part 2: CI/CD Pipeline**  
  Design and implement an efficient CI/CD pipeline that leverages the monorepo structure for optimal build performance, caching, and developer experience.

## Starter Pack

Our starter pack has the following structure:

```
repo/
  data-processor/
    main.py              # FastAPI data transformation service
    requirements.txt     # pandas==1.5.3, fastapi==0.95.0, pytest==7.1.0
    utils/               # Shared utilities (duplicated)
    tests/
  model-service/
    main.py              # ML inference service
    requirements.txt     # pandas==2.0.1, fastapi==0.100.0, pytest==7.4.0
    utils/               # Identical duplicate of data-processor/utils/
    tests/
  SOLUTION.md            ← you write this
  README.md
  ASSIGNMENT.md
```

**🎯 Current challenges:**
- 🔄 Code duplication: Identical `utils/` folders in both projects
- ⚡ Dependency conflicts: Different versions of pandas, fastapi, pytest, requests, uvicorn
- 🔧 Inconsistent tooling: Separate testing, linting, formatting configurations
- 📦 No build optimization: Each project builds independently with no shared caching

Feel free to organize your files whichever way you see fit.

## Environment Assumptions

Local development is fine, but feel free to use any platform you have readily available.

- **Monorepo tools**: [Pants](https://www.pantsbuild.org/), [Poetry workspaces](https://python-poetry.org/docs/managing-dependencies/#dependency-groups), [Bazel](https://bazel.build/), [Nx](https://nx.dev/), [Rush](https://rushjs.io/), or others of your choice
- **CI/CD platforms**: [GitHub Actions](https://docs.github.com/en/actions), [GitLab CI](https://docs.gitlab.com/ee/ci/), [Jenkins](https://www.jenkins.io/), or local simulation
- **Package managers**: [pip](https://pip.pypa.io/), [Poetry](https://python-poetry.org/), [uv](https://github.com/astral-sh/uv), [conda](https://docs.conda.io/), or others
- If you can't run a full CI/CD pipeline, you may provide configuration files and describe the expected behavior; note any assumptions.

## What to Submit

- A zip file or repository with:
  - Your monorepo configuration and restructured codebase
  - CI/CD pipeline configuration files
  - Setup and usage commands
  - `SOLUTION.md` covering design decisions, trade-offs, and instructions

## Next Steps

1. 📋 Read the detailed requirements in `ASSIGNMENT.md`
2. 💻 Implement your solution
3. 📝 Document your approach in `SOLUTION.md`

**Good luck! We're excited to see your approach to production-grade CI/CD infrastructure.**
