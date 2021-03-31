FROM ubuntu

WORKDIR /workdir


ENV PYTHONPATH /workdir
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python2 curl git
RUN curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py
RUN python2 get-pip.py
COPY server_package/serverreqs.txt serverreqs.txt
RUN python3 -m pip install -r serverreqs.txt
##RUN python3 -m pip install git+https://git.snt.utwente.nl/s2174294/reporttree
COPY treepackage /treepackage
RUN python3 -m pip install -e ../treepackage
# Clonen met ssh?
RUN git clone https://git.snt.utwente.nl/s2174294/nlpbreastcancer.git /workdir/nlp
RUN python2 -m pip install -r nlp/nlpreqs.txt
RUN python2 -c "import nltk; nltk.download('stopwords')"
RUN python2 -c "import nltk; nltk.download('averaged_perceptron_tagger')"
COPY server_package /workdir/servpackage

CMD ["python3", "./servpackage/server.py"]

