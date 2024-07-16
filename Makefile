update:
	@poetry update

# Clean .pyc
clean:
	@echo "Cleaning cache..."
	@find . | egrep '.pyc|.pyo|pycache' | xargs rm -rf
	@find . | egrep '.pyc|.pyo|pycache|pytest_cache' | xargs rm -rf
	@rm -rf ./pycache
	@rm -rf ./.pytest_cache
	@rm -rf ./.mypy_cache
	@echo "Cache cleared!"

# Tool For Style Guide Enforcement
format:
	@echo "Start isort execution:"
	@poetry run isort ./apps
	@echo "Finished isort execution."
	@echo ""

	@echo "Start black execution:"
	@poetry run black ./apps  --target-version py310
	@echo "Finished black execution."
	@echo ""

checker:
	@echo "Start flake8 execution:"
	@poetry run flake8 ./apps
	@echo "Finished flake8 execution."
	@echo ""

	@echo "Start pylint execution:"
	@poetry run pylint ./apps/
	@echo "Finished pylint execution."
	@echo ""

	@echo "Start mypy execution:"
	@poetry run mypy ./apps/
	@echo "Finished pylint execution."
	@echo ""

	@echo "Start bandit execution:"
	@poetry run bandit -v -r ./apps/ -c "pyproject.toml"
	@echo "Finished bandit execution."
	@echo ""

# Run app local
run:
	python manage.py runserver

# Dev tools
localdb:
	@docker run --name post_dev --rm -e POSTGRES_USER=post_dev -e POSTGRES_PASSWORD=post_dev -p 5432:5432 -v "blog-post:/var/lib/postgresql/data" -it postgres:15-alpine

docker-build:
	@docker build -t blog-app .

docker-run:
	@docker run -it -p 8000:8000 blog-app

# Tests Commands
test:
	@poetry run pytest --cov

test-report:
	@poetry run pytest --cov-report html --cov

run_prod:
	python manage.py makemigrations --merge --noinput
	python manage.py migrate
	python manage.py collectstatic --noinput
	gunicorn blog.wsgi -c ./blog/gunicorn.py
