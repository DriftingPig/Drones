/*******************************************************
**                                                    **
**     Load the configuration from a file             **
**     Author: Cheng Zhao <zhaocheng03@gmail.com>     **
**                                                    **
*******************************************************/

#ifndef _LOAD_CONF_H_
#define _LOAD_CONF_H_

#include "define.h"

typedef enum {
  parse_conf_start = 1,
  parse_conf_keyword = 2,
  parse_conf_equal = 3,
  parse_conf_value_start = 4,
  parse_conf_value_quote = 5,
  parse_conf_value = 6,
  parse_conf_done = 0,
  parse_conf_abort = -1
} PARSE_CONF_STATE;

typedef struct {
  int format;                           // FILE_TYPE
  int force;                            // FORCE
  int verbose;                          // VERBOSE
  char comment;                         // COMMENT
  char list[FLEN_FILENAME];             // BRICK_LIST
  char bdir[FLEN_FILENAME];             // BRICK_DIR
  char input[FLEN_FILENAME];            // INPUT
  char output[FLEN_FILENAME];           // OUTPUT
} CONF;


void init_conf(CONF *);

void read_opt(const int, char * const [], char *, CONF *);

int read_conf(const char *, CONF *);

int parse_conf(const char *, char *, char *, const size_t, const size_t,
    const size_t);

int check_conf(CONF *);

int check_input(const char *, const char *);

int check_output(const char *, const char *, const int);

void print_conf(const char *, const CONF *);

void temp_conf(void);

void usage(char *);

#endif

