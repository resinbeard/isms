TARGET_EXEC ?= isms
BUILD_DIR ?= ./build
SRC_DIRS ?= ./src

SRCS := $(shell find $(SRC_DIRS) -name *.cpp -or -name *.c -or -name *.s)
OBJS := $(SRCS:%=$(BUILD_DIR)/%.o)

DEPS := $(OBJS:.o=.d)

INC_DIRS := $(shell find $(SRC_DIRS) -type d)
INC_FLAGS := $(addprefix -I,$(INC_DIRS))

#CPPFLAGS = $(INC_FLAGS) -MMD -MP -ggdb
CFLAGS=-I/usr/include -I/usr/local/include -I/usr/include/lua5.4/ -std=c11 -Wall \
			 -L/usr/local/lib -lSDL2 -llua -lm -ldl -llo -lmonome -lasound \
			 -pthread -D_GNU_SOURCE

# main target (C)
$(BUILD_DIR)/$(TARGET_EXEC): $(OBJS)
	$(CC) $(OBJS) -o $@ $(LDFLAGS) $(CFLAGS)

# c source
$(BUILD_DIR)/%.c.o: %.c
	$(MKDIR_P) $(dir $@)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

gentoo:
	ln -s /usr/lib64/liblua5.4.so /usr/lib64/liblua.so

core:
	echo 'const char* core = " \' > src/core.h
	sed -e 's/$$/\ \\/' src/core.lua >> src/core.h
	echo '";' >> src/core.h


.PHONY: clean
clean:
	$(RM) -r $(BUILD_DIR)

-include $(DEPS)

MKDIR_P ?= mkdir -p


.PHONY: run
run: $(BIN)
	./build/isms


