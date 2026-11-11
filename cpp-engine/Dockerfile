FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

# Build the C++ engine
RUN cmake -B build -S . -DCMAKE_BUILD_TYPE=Release && \
    cmake --build build --target aether_engine -j 4

EXPOSE 8080
CMD ["./build/aether_engine"]