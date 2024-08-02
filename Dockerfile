ARG BUILD_DIR="/build"
ARG APP_DIR="$BUILD_DIR/app"
ARG UI_DIR="$BUILD_DIR/ui"

FROM python:3.12.4-bookworm AS build-image

RUN apt-get update && apt-get install -y npm
# Install nodejs LTS version
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash -
RUN apt-get install -y nodejs

ARG BUILD_DIR
ARG APP_DIR
ARG UI_DIR
RUN mkdir -p $BUILD_DIR

COPY app/requirements.txt $BUILD_DIR
RUN pip install -r "$BUILD_DIR/requirements.txt" --target $APP_DIR

COPY app "$APP_DIR/"
COPY ui "$UI_DIR/"

WORKDIR $UI_DIR
RUN npm install
#RUN npm audit fix
RUN npx browserslist@latest --update-db
RUN npm run build

#COPY api_credentials.json $BUILD_DIR

FROM python:3.12.4-slim-bookworm

ARG BUILD_DIR
ARG APP_DIR
ARG UI_DIR

RUN mkdir -p $BUILD_DIR
COPY --from=build-image $APP_DIR $APP_DIR
COPY --from=build-image "$UI_DIR/build" "$UI_DIR/build"
COPY api_key.json $APP_DIR
RUN chmod +x "$APP_DIR/run.sh"

WORKDIR $APP_DIR
ENV PYTHONPATH=$BUILD_DIR

CMD ["./run.sh"]
