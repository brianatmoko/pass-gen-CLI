CXX := g++
CXXFLAGS := -O2 -fPIC -Wall -Wextra
LDFLAGS := -shared

TARGET := libpassgen.so

.PHONY: all clean

all: $(TARGET)

$(TARGET): engine.cpp engine.h
	$(CXX) $(CXXFLAGS) $(LDFLAGS) -o $@ engine.cpp

clean:
	rm -f $(TARGET)
