FROM ubuntu:18.04

#MAINTAINER Bitroot Developers <dev@bitroot.io>

# Install common dependencies
RUN apt-get update && apt-get install -y apt-utils ca-certificates wget curl git mercurial \
    python3 python3-dev python3-pip python3-setuptools python3-appdirs \
    build-essential vim unzip software-properties-common sudo gettext-base \
    net-tools iputils-ping telnet lynx locales

# Upgrade pip3 to newest
RUN pip3 install --upgrade pip

# Set locale
RUN dpkg-reconfigure -f noninteractive locales && \
    locale-gen en_US.UTF-8 && \
    /usr/sbin/update-locale LANG=en_US.UTF-8
ENV LC_ALL en_US.UTF-8

# Set home dir env variable
ENV HOME /root

# Install bitroot-lib
COPY . /bitroot-lib
WORKDIR /bitroot-lib
RUN pip3 install -r requirements.txt
RUN python3 setup.py develop
RUN python3 setup.py install_apsw

# Install Bitroot-cli
# NOTE: By default, check out the Bitroot-cli master branch. You can override the BRANCH build arg for a different
# branch (as you should check out the same branch as what you have with bitroot-lib, or a compatible one)
# NOTE2: In the future, bitroot-lib and Bitroot-cli will go back to being one repo...
ARG CLI_BRANCH=master
ENV CLI_BRANCH ${CLI_BRANCH}
RUN git clone -b ${CLI_BRANCH} https://github.com/BitrootD/Bitroot-cli.git /Bitroot-cli
WORKDIR /Bitroot-cli
RUN pip3 install -r requirements.txt
RUN python3 setup.py develop

# Additional setup
COPY docker/server.conf /root/.config/bitroot/server.conf
COPY docker/start.sh /usr/local/bin/start.sh
RUN chmod a+x /usr/local/bin/start.sh
WORKDIR /

EXPOSE 4000 14000

# NOTE: Defaults to running on mainnet, specify -e TESTNET=1 to start up on testnet
ENTRYPOINT start.sh ${BTC_NETWORK} ${NO_BOOTSTRAP}
