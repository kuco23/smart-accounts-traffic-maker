FROM python:3.13-alpine AS base

# Setup env
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1

FROM base AS build

COPY . /app/

FROM base AS python-deps

COPY Pipfile .
COPY Pipfile.lock .
RUN apk update && \
    apk add --no-cache gcc && \
    pip install pipenv && \
    PIPENV_VENV_IN_PROJECT=1 pipenv install --python 3.13 --deploy

FROM build AS submodule

WORKDIR /app/smart_accounts_cli
RUN apk add --no-cache git && \
    git submodule update --init --recursive && \
    python -m venv .venv && \
    ./.venv/bin/pip install -r requirements.txt

FROM base AS runner

# set workdir
WORKDIR /app

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Copy submodule
COPY --from=submodule /app/smart_accounts_cli ./smart_accounts_cli

# Copy python executables
COPY --from=build /app/qa_lib/ ./qa_lib/
COPY --from=build /app/cli/ ./cli/
COPY --from=build /app/artifacts/ ./artifacts/

# copy entrypoint
COPY --from=build /app/entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]