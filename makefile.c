makefile
CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -Iinclude
TARGET = bitcalc
SRCS = src/main.c src/converters.c src/bit_utils.c src/ui.c
OBJS = $(SRCS:.c=.o)

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(OBJS) -o $(TARGET)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)

run: $(TARGET)
	./$(TARGET)

.PHONY: all clean run
