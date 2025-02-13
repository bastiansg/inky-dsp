FROM inkywhat-dsp/core

COPY inkywhat_dsp /src/inkywhat_dsp
COPY requirements.txt pyproject.toml  /src/
RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,source=.git,target=/src/.git \
    pip install /src --no-deps

WORKDIR /src/inkywhat_dsp/api
CMD fastapi run app.py
