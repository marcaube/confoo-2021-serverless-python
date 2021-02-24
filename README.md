# Python on AWS Lambda using Chalice

Just a toy application for my introduction to serverless @ Confoo 2021. [See the slides](https://speakerdeck.com/marcaube/going-serverless-with-python).


## Prerequisites
- [AWS cli](https://aws.amazon.com/cli/) (installed and configured)
- [Chalice](https://aws.github.io/chalice/index)
- python 3.8


## Installation
First, start by creating a virtual environment to prevent installing the dependencies globally on your system.

```bash
$ make venv
```

Activate that virtual environment

```bash
$ source .venv/bin/activate
```

Install the project dependencies

```bash
$ make install
```


## Deployment

Export your AWS profile

```bash
$ export AWS_PROFILE=chalice-hello
```

Deploy your functions

```bash
$ chalice deploy
```
