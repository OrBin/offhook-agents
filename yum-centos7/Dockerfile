FROM centos:7

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN yum install -y epel-release \
    && yum install -y https://www.elrepo.org/elrepo-release-7.0-4.el7.elrepo.noarch.rpm \
    && yum install -y python-pip p7zip p7zip-plugins \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn==19.10.0

COPY . /usr/src/app

EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "swagger_server.__main__:app"]
