# ==============================================================
# Kaiko Monorepo - Local CI Makefile
# ==============================================================

SHELL := /bin/bash
UV_BIN := $(HOME)/.local/bin/uv
SERVICES := $(notdir $(wildcard services/*))

# --------------------------------------------------------------
# 🧰 Setup
# --------------------------------------------------------------

.PHONY: setup
setup:
	@echo "🔧 Installing required tools..."
	command -v curl >/dev/null 2>&1 || (echo "❌ curl not found"; exit 1)

	# ------------------------------------------------------------
	# Install uv
	# ------------------------------------------------------------
	@if [ ! -f "$(HOME)/.local/bin/uv" ]; then \
		echo "⬇️  Installing uv..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	else \
		echo "✅ uv already installed."; \
	fi

	# ------------------------------------------------------------
	# Ensure ~/.local/bin exists and is on PATH
	# ------------------------------------------------------------
	mkdir -p $(HOME)/.local/bin
	export PATH="$(HOME)/.local/bin:$$PATH"

	# ------------------------------------------------------------
	# Install act into ~/.local/bin
	# ------------------------------------------------------------
	@if ! command -v act >/dev/null 2>&1; then \
		echo "⬇️  Installing act..."; \
		curl -Ls https://raw.githubusercontent.com/nektos/act/master/install.sh | bash -s -- -b $(HOME)/.local/bin; \
	else \
		echo "✅ act already installed."; \
	fi

	# ------------------------------------------------------------
	# Sync dependencies and install pre-commit
	# ------------------------------------------------------------
	$(HOME)/.local/bin/uv sync
	$(HOME)/.local/bin/uv run pre-commit install
	@echo "✅ Setup complete! Ready for local CI."
# --------------------------------------------------------------
# 🧼 Linting and Formatting
# --------------------------------------------------------------

.PHONY: lint
lint:
	@echo "🧹 Running Ruff linter..."
	$(UV_BIN) run ruff check .

.PHONY: format
format:
	@echo "🧾 Checking code formatting..."
	$(UV_BIN) run ruff format --check .

.PHONY: fix
fix:
	@echo "🪄 Auto-fixing lint and formatting issues..."
	$(UV_BIN) run ruff check --fix .
	$(UV_BIN) run ruff format .

# --------------------------------------------------------------
# 🧪 Testing
# --------------------------------------------------------------

.PHONY: test
test:
	@ uv sync --frozen
	@for svc in $(SERVICES); do \
		echo "🚀 Running tests for service: $$svc"; \
		( cd services/$$svc && $(UV_BIN) run pytest -v ) || exit 1; \
	done
	@echo "✅ All tests completed successfully!"

# --------------------------------------------------------------
# 🧩 Run full CI locally (simulate GitHub Actions)


.PHONY: ci
ci:
	@echo "🏗️  Running full CI pipeline locally using act..."
	PATH="$(HOME)/.local/bin:$$PATH" act --container-architecture linux/amd64 --pull=false --artifact-server-path ./.tmp/artifacts
	@echo "🎉 Local CI completed successfully!"

# --------------------------------------------------------------
# 🧹 Cleanup
# --------------------------------------------------------------

.PHONY: clean
clean:
	@echo "🧽 Cleaning project..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".tmp" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup complete."
