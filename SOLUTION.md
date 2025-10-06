# Solution

Before starting the two main parts of the assignment, I first verified that the existing setup worked as expected, prior to converting it into a monorepo.
I created a Python environment and attempted to install the dependencies, but the installation failed because no Python version was specified and my initial choice (Python 3.13) was incompatible with some dependencies.

Both services were also missing the `httpx` sub-dependency required for testing (it’s used by `starlette`, a dependency of FastAPI).
I resolved this by installing `fastapi` with the `standard-no-fastapi-cloud-cli` extras, which include the necessary testing dependencies such as `httpx` and `uvicorn` — [FastAPI reference](https://fastapi.tiangolo.com/?h=httpx#standard-dependencies).

In addition, the `model-service` contained a failing test where the expected status code was `404` but the service returned `400`. This happened because an exception was raised inside a try block where it should have been handled outside the try block.
The same service was also missing `import uvicorn`, and both services included an unused dependency on `requests`.

After addressing these issues, I confirmed that both services were functional and ready to be migrated into a unified monorepo structure.


## Part 1 - Monorepo Setup

### Tool Selection

I have not worked on a monorepo before so I had to do some research to understand how multiple environments are managed. I choose `UV` because it is unifies multiple python tools into one and is super fast. Since the repo is using only `python` and  the services have a lot of common packages that can be shared and do not rely on specific version to run, I decided that `UV` is a good choice for this small project. `UV` supports workspaces and a single lock file for the whole repo, which is an advantage for this project because any developer can replicate the environment from a single command by sync-ing with the root lock file.

### Architecture Decisions

The first step was to restructure the repository into a monorepo. I introduced two top-level directories: `libs` for shared libraries and `services` for all project services. The existing `utils` module was moved into `libs/utils` (and removed from both services), while `data_processor` and `model_service` were moved under `services/`.

Once the structure was established, I verified that both services still functioned correctly. To make the shared code importable, I converted `utils` into a proper Python package rather than a collection of scripts. I also converted each service and their tests into packages by adding an` __init__.py` file, ensuring pytest could discover tests from the repository root without any naming conflicts.

I then created a `pyproject.toml` for the root directory and for each service. The root configuration defines all shared dependencies (e.g., `fastapi`, `pandas`, `uvicorn`), development tools (`pytest`, `pytest-cov`, `ruff`, `pre-commit`), and the workspace layout. Each service’s `pyproject.toml` references the `utils` package from the `libs/utils` workspace and specifies any additional, service-specific dependencies.

During this process, I discovered that UV workspaces inherit dependencies from the root environment as long as uv sync is not run inside individual service directories. This means the correct workflow is to perform dependency synchronization once at the root level, after which commands can be executed from any workspace seamlessly.

Next, I validated dependency compatibility by upgrading all shared libraries to their latest versions. This helped confirm whether the monorepo could maintain unified versions across all services. Since no conflicts occurred and the assignment did not specify version constraints, I decided to use the latest versions (restricted to current major version) and keep the libraries shared at the root level. In a real-world scenario, where stricter dependency isolation might be required, each service would maintain its own locked dependency set, but for this setup, a shared configuration is both simpler and efficient.


### Implementation Details

Most of the commands used are done through `uv`, so make sure to install it. (It can be instaled with `make` in Part 2)

I will assume that UV is installed. See how to install [here](https://docs.astral.sh/uv/getting-started/installation/).

Here are some commands I have used.
```zsh
# Synchronise UV with the lock file from repo root directory
uv sync --frozen

# Run individual service
cd services/model_service
uv run main.py

# Run tests for a specific service
cd services/model_service
uv run pytest

# Run monorepo-wide operations
uv run --all-packages pytest
uv run ruff check .
uv run ruff format --check .
```

## Part 2 - CI/CD Pipeline

### Platform and Strategy

I chose GitHub Actions because it integrates seamlessly with GitHub, where this repository is hosted, and provides a wide range of built-in Actions that can be used out of the box without additional setup.

To avoid duplication, I created a reusable workflow template (`reusable-service-pipeline.yml`) that defines the steps required to build, lint, and test an individual service. Since all services share a similar structure, this approach allows each service to run through the same pipeline logic with minimal configuration. The workflow leverages cached data from `UV`, `ruff`, and `pytest` to reduce execution time across runs.

In the main `cicd.yaml` workflow, I define one job per service, running them in parallel to maximize efficiency. Each job is triggered only when relevant changes are detected — such as updates to the service’s own files, shared libraries, or the CI/CD configuration.

This setup could be further optimized by using a prebuilt container image containing all dependencies and tooling. During CI runs, the service directory could be mounted as a volume into this container, allowing tests to execute without rebuilding or reinstalling dependencies each time. This approach requires hosting the container image in a remote registry, but it would significantly reduce setup overhead in each pipeline run, with the cost of only pulling the image (which itself can be cached).

### Performance Analysis

The current state of the project already demonstrates several measurable improvements:
- There are no more duplicated libraries, which means less code to maintain and synchronize across services.
- The CI/CD pipeline can now test services in parallel and automatically skip those that have not changed.
- By leveraging cached data from previous runs, subsequent CI/CD executions are faster, as unchanged components are reused rather than rebuilt or retested.
- The global UV lock file keeps all dependencies centralized, reducing the likelihood of version drift or developer mistakes compared to maintaining separate lock files per service.
- The provided `Makefile` simplifies environment setup by installing all necessary tools and offering convenient commands for cleaning and testing the entire project. This significantly reduces the time developers spend on configuration and setup.
- The `pre-commit` configuration enables developers to catch linting and formatting issues before pushing changes, saving CI/CD resources and improving overall feedback time during development.

### Usage Instructions

```zsh
# Local development workflow
make setup # setup the environment by installing all needed tools and configuring them
make test
make clean

# Run CI pipeline locally
make ci # runs the CI/CD pipeline using act
# or make lint, make format, make fix

# Pre-commit setup
make setup # it installs the pre-commit
```

## Lessons Learned

- Challenges encountered and how they were solved

One of the main challenges was understanding how monorepo tools work and how they can be applied effectively. Different projects require different approaches, and since this was my first time setting up a monorepo, I faced some difficulties integrating all tools and shared libraries across services. Reading about UV workspaces and experimenting with configurations helped me understand how they function and how to adapt them for this project.

Another significant challenge was structuring the CI/CD pipeline. The main difficulty was the lack of context about how developers would actually use and extend it. In a real-world setting, I would collaborate closely with the development team to design a workflow that fits their daily processes. For this assignment, I had to make assumptions and implemented a general approach that tests all services uniformly — though in a larger project, a more selective or incremental testing strategy would be preferable.

- What I would do differently in a larger, real-world scenario

In a larger project, I would likely choose a different monorepo management tool. UV is fast and lightweight, but I discovered that some behaviors were either missing or worked differently than expected — for example, services not inheriting root-level dependencies automatically.

I would also containerize the development and CI environments using Docker, ensuring reproducibility across developer machines and CI runners. In the CI/CD pipelines, I would focus on building a single base image with all required tools preinstalled, to minimize setup time and improve consistency.

Finally, I would work closely with developers to understand their workflows and requirements, and design the CI/CD process to match how they actually build, test, and deploy code.

- Recommendations for scaling this approach

The current `cicd.yaml` workflow uses hardcoded service names to define the pipeline matrix. This approach works for a small number of services but does not scale well as the monorepo grows. A more dynamic solution would be to generate the matrix programmatically, for example by scanning the `services/` directory at runtime.

Some steps, such as linting and testing, can also be split into separate jobs to allow parallel execution and faster feedback. In a larger setup, each service should ideally be built as a container image and pushed to a remote registry. This allows tests to be run directly against those images without reinstalling dependencies, and the use of layered builds enables efficient caching — only the modified layers need to be rebuilt and pushed.
