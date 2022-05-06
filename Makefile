setup:
	./scripts/get_chromedriver.sh

env:
	poetry install

play-rubicon: copy play-using-policy

copy:
	cat js/auto-move-override.js | pbcopy

play-using-policy:
	poetry run python src/play_rubicon.py --policy $(POLICY)

lint:
	poetry run black src/
	poetry run isort src/
	poetry run flake8 --ignore=E501 src/

.PHONY: env copy play-rubicon play-using-policy