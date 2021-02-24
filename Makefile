install: venv
ifeq ($(VIRTUAL_ENV),)
	@echo "[!] Type '\033[0;32msource .venv/bin/activate\033[0m' to activate your virtual environment first, then '\033[0;32mmake install\033[0m' again."
else
	.venv/bin/python3 -m pip install -r requirements-dev.txt
	.venv/bin/python3 -m pip install -r requirements.txt
endif

venv:
ifeq ($(wildcard .venv),)
	@echo "[-] Creating a virtual environment in .venv/..."
	@test -d venv || python3 -m venv .venv
	@echo "[-] Updating pip..."
	@.venv/bin/python3 -m pip install -q --upgrade pip
	@echo "[-] Done!"
endif
