FROM mhart/alpine-node:10 as node
COPY package.json .
RUN yarn install

FROM flungo/inkscape as inkscape
RUN apk add --no-cache make
COPY Makefile .
COPY mapParts mapParts
RUN make svg2png

FROM python:3-alpine
RUN apk add --no-cache imagemagick make

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY Makefile index.html ./
COPY src src
COPY mapParts/legend.json mapParts/legend.json
COPY --from=node node_modules ./node_modules
COPY --from=inkscape mapParts/exports mapParts/exports

RUN make layers clean-temp

ENTRYPOINT ["make", "start"]