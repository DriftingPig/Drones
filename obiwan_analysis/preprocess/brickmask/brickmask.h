/**********************************************************
**                                                       **
**      Apply veto masks per brick to a galaxy catalog   **
**      Author: Cheng Zhao <zhaocheng03@gmail.com>       **
**                                                       **
**********************************************************/

#ifndef _BRICKMASK_H_
#define _BRICKMASK_H_

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <fitsio.h>
#include "define.h"
#ifdef OMP
#include <omp.h>
#endif

/********** read_data.c **********/

int read_ascii(const char *, const char, DATA **, size_t *, const int);

int read_fits(const char *, DATA **, size_t *, const int);

int read_list(const char *, char ***, double **, double **, double **,
    double **, size_t *, const int);

int read_wcs_header(fitsfile *, WCS *);

/********** read_data.c **********/

/********** baselib.c **********/

size_t safe_strcpy(char *, const char *, const size_t);

int wcs_world2pix(const WCS *, const double, const double, double *, double *);

/********** baselib.c **********/

/********** find_brick.c **********/

long find_brick(const double, const double, const double *, const double *,
    const double *, const double *, const size_t);

int compare_pos(const double, const double, const double, const double,
    const double, const double);

int compare_idx(const void *, const void *);

/********** find_brick.c **********/

/********** save_res.c **********/

int write_ascii(const char *, const DATA *, const size_t, const int);

int write_fits(const char *, const char *, const DATA *, const long, const int);

/********** save_res.c **********/

#endif
