ARG GO_VERSION=1.19
ARG ALPINE_VERSION=3.17

# build-stage

FROM golang:${GO_VERSION}-alpine${ALPINE_VERSION} as build-stage

WORKDIR /app

COPY go.mod .
COPY go.sum .

RUN go mod download

COPY . .

RUN go build -o extract

# production-stage

FROM alpine:${ALPINE_VERSION} as production-stage

RUN addgroup appgroup && adduser --disabled-password --no-create-home appuser -G appgroup

WORKDIR /app

COPY --from=build-stage /app/extract .

COPY templates/ templates/

RUN chmod 771 ./extract

RUN chmod 444 ./templates/index.html

RUN echo "FLAG{ex7r4c7_1s_br0k3n_by_b4d_p4r4m3t3rs}" > /flag

RUN chmod 664 /flag

USER appuser

CMD ./extract
