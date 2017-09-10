# gatecoin-automation

[![Known Vulnerabilities](https://snyk.io/test/github/thomasmktong/gatecoin-automation/badge.svg)](https://snyk.io/test/github/thomasmktong/gatecoin-automation)

## Install

```
$ pip install -r requirements.txt
$ cp config.template.yml config.yml
```

## Run

```
$ apistar run

Running at http://localhost:8080/
API doc at http://localhost:8080/api/docs/
```

## Continuous Integration

* Changes on `master` are automatically deployed to https://gatecoin-automation.herokuapp.com/
* Vulnerabilities of pip requirements are checked in Snyk.io

## Reference

* API Star: https://github.com/encode/apistar
* D3 Gallery: https://github.com/d3/d3/wiki/Gallery
* Gatecoin API: https://gatecoin.com/api
