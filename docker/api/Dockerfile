FROM inky-dsp/core

COPY inky_dsp /src/inky_dsp
COPY requirements.txt pyproject.toml  /src/
RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,source=.git,target=/src/.git \
    pip install /src --no-deps

WORKDIR /src/inky_dsp/api
CMD fastapi run app.py
