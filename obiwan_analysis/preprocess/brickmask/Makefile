CC = gcc
LIBS = -lm -lcfitsio #-fopenmp 
INCL = 
OPTS = -O3 -Wall $(INCL) $(LIBS) #-DOMP
SRCS = baselib.c brickmask.c find_brick.c load_conf.c read_data.c save_res.c
EXEC = vetomask

all:
	$(CC) $(SRCS) -o $(EXEC) $(OPTS)

clean:
	rm -f $(EXEC)

