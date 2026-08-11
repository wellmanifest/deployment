FROM python:3.12.11-alpine3.22@sha256:efcdfa6a6b2fd2afb9c7dfa9a5b288a6f68338b5cfdebe6b637d986067d85757

ADD --checksum=sha256:90d8d6d413945287df8c79fb115fafbea284af2b715c6a979d8ed1d1a30d3a72 \
  https://raw.githubusercontent.com/wellmanifest/dsl/550e5f441c709e15f2679c1af151352d1eba2f1e/src/dsl_check.py \
  /opt/wellmanifest/dsl_check.py

WORKDIR /workspace
COPY . /workspace

CMD ["python3", "/opt/wellmanifest/dsl_check.py", "validate", "--root", ".", "dsl-manifest.json"]
