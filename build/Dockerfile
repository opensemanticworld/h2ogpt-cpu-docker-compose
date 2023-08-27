FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    software-properties-common \
    make \
    gcc \
    g++

ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py310_23.1.0-1-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-py310_23.1.0-1-Linux-x86_64.sh -b \
    && rm -f Miniconda3-py310_23.1.0-1-Linux-x86_64.sh

#RUN conda create -n h2ogpt -y \
#     && echo "source activate env" > ~/.bashrc
#    && conda activate h2ogpt \
#    && conda install python=3.10 -c conda-forge -y

#RUN conda install python=3.10 -c conda-forge -y

RUN conda create -n h2ogpt -y
# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "h2ogpt", "/bin/bash", "-c"]
RUN conda install python=3.10 -c conda-forge -y

RUN git clone https://github.com/h2oai/h2ogpt.git \
    && cd h2ogpt \
    && pip uninstall -y pandoc pypandoc pypandoc-binary \
    # CPU only
    && pip install -r requirements.txt --extra-index https://download.pytorch.org/whl/cpu

RUN cd h2ogpt \
    # May be required for jq package:
    && apt-get install -y autoconf libtool \
    # Required for Doc Q/A: LangChain:
    && pip install -r reqs_optional/requirements_optional_langchain.txt \
    # Required for CPU: LLaMa/GPT4All:
    && pip install -r reqs_optional/requirements_optional_gpt4all.txt \
    # Optional: PyMuPDF/ArXiv:
    && pip install -r reqs_optional/requirements_optional_langchain.gpllike.txt \
    # Optional: Selenium/PlayWright:
    && pip install -r reqs_optional/requirements_optional_langchain.urls.txt \
    # Optional: support docx, pptx, ArXiv, etc. required by some python packages
    && apt-get update \
    && apt-get install -y libmagic-dev poppler-utils tesseract-ocr libtesseract-dev libreoffice \
    # Improved OCR with DocTR:
    && pip install -r reqs_optional/requirements_optional_doctr.txt \
    # go back to older onnx so Tesseract OCR still works
    && pip install onnxruntime==1.15.0 onnxruntime-gpu==1.15.0 \
    # Optional: for supporting unstructured package
    && python -m nltk.downloader all \
    # Optional but required for PlayWright
    && playwright install --with-deps

# install Chrome for Selenium (TODO: Replace with OpenSource alternative)
RUN apt-get update \
    && apt install -y unzip xvfb libxi6 libgconf-2-4 \
    && apt install -y default-jdk \
    && curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add \
    && bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list" \
    && apt -y update \
    && apt -y install google-chrome-stable \
    && CHROMEVER=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") \
    && DRIVERVER=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_$CHROMEVER") \
    && wget "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$DRIVERVER/linux64/chromedriver-linux64.zip" \
    && unzip chromedriver-linux64.zip \
    && mv chromedriver-linux64/chromedriver /usr/bin/chromedriver \
    && chown root:root /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver \
    && rm -R chromedriver-linux64

# preload model (~7GB => skip and download on demand at runtime)
#RUN \
#    && wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/resolve/main/llama-2-7b-chat.ggmlv3.q8_0.bin

#RUN cd h2ogpt \
#    && mkdir "userdata" \
#    && echo "A XYZ-Document is document containing only the letters X,Y and Z" >> "userdata/test.txt"

#EXPOSE 7860

ENTRYPOINT [\
    "conda", "run", "--no-capture-output", "-n", "h2ogpt", \
    "python", "h2ogpt/generate.py", \
    "--base_model='llama'", \
    "--prompt_type=llama2", \
    "--score_model=None", \
    "--langchain_mode='UserData'", \
    "--user_path=userdata" \
]