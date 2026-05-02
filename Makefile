.PHONY: install-test install help

install-test:
	pip install -r requirements.txt --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/

install:
	pip install -r requirements.txt

help:
	python .\src\bench.py --help

list-sdks:
	python .\src\bench.py --list-sdks

bench-static-bool:
	python .\src\bench.py --sdk static-bool --processes 1 --values 5 --warmups 1 --min-time 1.0

bench-switcher-client:
	python .\src\bench.py --sdk switcher-client --processes 1 --values 5 --warmups 1 --min-time 1.0

bench-harness-featureflags:
	python .\src\bench.py --sdk harness-featureflags --processes 1 --values 5 --warmups 1 --min-time 1.0

bench-unleash-client:
	python .\src\bench.py --sdk unleash-client --processes 1 --values 5 --warmups 1 --min-time 1.0

bench-optimizely-sdk:
	python .\src\bench.py --sdk optimizely-sdk --processes 1 --values 5 --warmups 1 --min-time 1.0

bench-amplitude-experiment:
	python .\src\bench.py --sdk amplitude-experiment --processes 1 --values 5 --warmups 1 --min-time 1.0

bench-splitio-client:
	python .\src\bench.py --sdk splitio-client --processes 1 --values 5 --warmups 1 --min-time 1.0
