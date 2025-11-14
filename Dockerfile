FROM nginx:alpine
RUN echo '<h1>Hello from Kubernetes!</h1>' > /usr/share/nginx/html/index.html
