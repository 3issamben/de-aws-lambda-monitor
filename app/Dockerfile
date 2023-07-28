# Use a specific version of the AWS provided Python Lambda base image
FROM public.ecr.aws/lambda/python@sha256:7f867f958f685d4321e4520e20b13900a47210ee57b3e41d05395b11f4c93c70 as build

# Install unzip utility, download Chrome and ChromeDriver, then unzip them to the /opt/ directory
RUN yum install -y unzip tar bzip2 gzip

RUN curl -Lo "/tmp/chromedriver.zip" "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip" && \
    curl -Lo "/tmp/chrome-linux.zip" "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F1135561%2Fchrome-linux.zip?alt=media" && \
    unzip /tmp/chromedriver.zip -d /opt/ && \
    unzip /tmp/chrome-linux.zip -d /opt/


ARG FIREFOX_VERSION=115.0.3
ARG GECKODRIVER=0.33.0

RUN curl -Lo "/tmp/firefox.tar.bz2" "https://ftp.mozilla.org/pub/firefox/releases/${FIREFOX_VERSION}/linux-x86_64/en-US/firefox-${FIREFOX_VERSION}.tar.bz2" \
    && curl -Lo "/tmp/geckodriver.tar.gz" "https://github.com/mozilla/geckodriver/releases/download/v${GECKODRIVER}/geckodriver-v${GECKODRIVER}-linux64.tar.gz" \
    && tar xvjf /tmp/firefox.tar.bz2 -C /opt \
    && tar -xzf /tmp/geckodriver.tar.gz -C /opt \
    && rm /tmp/firefox.tar.bz2 \
    && rm /tmp/geckodriver.tar.gz


# Use the same base image to create a new build stage
FROM public.ecr.aws/lambda/python@sha256:7f867f958f685d4321e4520e20b13900a47210ee57b3e41d05395b11f4c93c70

# Install necessary dependencies for Chrome and ChromeDriver
RUN yum install atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    libgtk-3-0 libdbus-glib-1-2 \
    xorg-x11-xauth dbus-glib dbus-glib-devel -y

# Copy the Chrome and ChromeDriver binaries from the previous build stage
COPY --from=build /opt/chrome-linux /opt/chrome
COPY --from=build /opt/chromedriver /opt/
# Copy the firefox and geckodriver binaries from the previous build stage
COPY --from=build /opt/firefox /opt/firefox
COPY --from=build /opt/geckodriver /opt/geckodriver

ENV PATH="/opt/firefox/firefox:${PATH}"

# Install python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy your Python script
COPY *.py ${LAMBDA_TASK_ROOT}

# Set the command to be executed when running the container
CMD [ "main.lambda_handler" ]
