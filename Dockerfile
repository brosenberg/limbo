FROM gliderlabs/alpine:3.3

ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# get our basic-needs sorted
RUN apk-install python3 python3-dev vim bash    \
                curl      \
    && curl "https://bootstrap.pypa.io/get-pip.py" | python3 \
    && pip install --upgrade pip setuptools     \
    && ln -s /usr/bin/python3 /usr/bin/python   \
    && mkdir -p /opt /app

ADD . /app
WORKDIR /app
RUN pip install -e .
CMD /app/bin/kube-limbo

# vim: set expandtab tabstop=4 shiftwidth=4 autoindent smartindent:
