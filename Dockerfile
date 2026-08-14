FROM python:3.12.11-alpine3.22@sha256:efcdfa6a6b2fd2afb9c7dfa9a5b288a6f68338b5cfdebe6b637d986067d85757

ADD --checksum=sha256:90d8d6d413945287df8c79fb115fafbea284af2b715c6a979d8ed1d1a30d3a72 \
  https://raw.githubusercontent.com/wellmanifest/dsl/550e5f441c709e15f2679c1af151352d1eba2f1e/src/dsl_check.py \
  /opt/wellmanifest/dsl_check.py

ADD --checksum=sha256:cf9416ae496666092d3109f0d937a66faecc486cf7d84c74e38de6154fa7fdf1 \
  https://raw.githubusercontent.com/wellmanifest/dsl/b7d0595c95e5abbb48ebfdbdae0bc6d43c6f82f4/src/dsl_check.py \
  /opt/wellmanifest/dsl_check-b7d059.py

WORKDIR /workspace
COPY . /workspace

CMD ["python3", "-c", "import json, runpy, sys; schema=json.load(open('dsl-manifest.json', encoding='utf-8')).get('$schema'); profiles={'https://raw.githubusercontent.com/wellmanifest/dsl/550e5f441c709e15f2679c1af151352d1eba2f1e/schemas/dsl-manifest.schema.json':('/opt/wellmanifest/dsl_check.py',['validate','--root','.','dsl-manifest.json']),'https://raw.githubusercontent.com/wellmanifest/dsl/b7d0595c95e5abbb48ebfdbdae0bc6d43c6f82f4/schemas/dsl-manifest.schema.json':('/opt/wellmanifest/dsl_check-b7d059.py',['validate','dsl-manifest.json'])}; selected=profiles.get(schema); selected or sys.exit('DSL-MANIFEST-001: unsupported immutable manifest schema '+repr(schema)); script,args=selected; sys.argv=[script,*args]; runpy.run_path(script,run_name='__main__')"]
