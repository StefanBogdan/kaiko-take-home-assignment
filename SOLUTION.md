# Solution

> Replace this template with your implementation details and design decisions.

## Part 1 - Monorepo Setup

### Tool Selection

**Chosen tool**: [Your choice: Pants, Poetry workspaces, etc.]

**Rationale**:
- Explain why you selected this tool
- How it addresses the specific challenges of this project
- Trade-offs compared to other options

### Architecture Decisions

**Dependency Resolution**:
- How you resolved version conflicts
- Final dependency versions chosen and why

**Shared Code Organization**:
- How you restructured the duplicated utils code
- Import strategy and package organization

**Build Configuration**:
- How you configured builds, tests, and tooling
- Any project-specific customizations

### Implementation Details

Provide the commands to:
```bash
# Set up the development environment
[your commands here]

# Run individual service
[your commands here]

# Run tests for a specific service
[your commands here]

# Run monorepo-wide operations
[your commands here]
```

## Part 2 - CI/CD Pipeline

### Platform and Strategy

**Chosen platform**: [GitHub Actions, GitLab CI, etc.]

**Architecture overview**:
- Pipeline stages and their purpose
- Parallelization strategy
- Caching approach

### Optimization Techniques

**Build efficiency**:
- How you minimized startup overhead
- Strategies for incremental builds
- Caching implementation details

**Change detection**:
- How the pipeline determines what to test/build
- Affected project detection logic

### Performance Analysis

**Expected improvements**:
- Estimated time savings compared to separate project builds
- Resource utilization improvements
- Developer experience enhancements

### Usage Instructions

```bash
# Local development workflow
[your commands here]

# Run CI pipeline locally
[your commands here]

# Pre-commit setup
[your commands here]
```

## Lessons Learned

- Challenges encountered and how you solved them
- What you would do differently in a larger, real-world scenario
- Recommendations for scaling this approach
