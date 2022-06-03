install:
	#install commands
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	#format code
	black *.py stock_view/*.py
lint:
	pylint --disable=R,C,broad-except *.py stock_view/*.py
test:
	#test
build:
	#build container
	docker build -t stock_view:latest .
run:
	#run container
	docker run -p 8501:8501 stock_view:latest
deploy:
	#deploy
all:install format lint build run


