/*******************************************************
**                                                    **
**     Common definitions (macros) for brickmask      **
**     Author: Cheng Zhao <zhaocheng03@gmail.com>     **
**                                                    **
*******************************************************/

#ifndef _DEFINE_H_
#define _DEFINE_H_

#include <stdlib.h>

/******************************************************************************
  Definitions for mask files and bit codes.
******************************************************************************/
#define NUMSUB  4       // Number of sub-samples.
#define SUB_FNAME {             \
  "mask-eboss21-%s.fits.gz",    \
  "mask-eboss22-%s.fits.gz",    \
  "mask-eboss23-%s.fits.gz",    \
  "mask-eboss25-%s.fits.gz"}    // Filename of sub-samples.
#define MASK_VALID (bit & 1)    // Assign only valid maskbits to inputs.
#define XYBUG 4         // Bit code for xybug. It is specially treated since
                        // the coordinates are truncated in this case.
                        // (They are rounded in the usual case.)
                        // Disable this feature by setting a negative value.
#define XYBUG_VALID (bit >> 2 & 1)      // Check if XYBUG = 4 presents.

/******************************************************************************
  Definitions for runtime constants.
******************************************************************************/
#define INIT_INT -10    // Initial (invalid) value for intergers.
#define TIMEOUT  10     // Maximum number of input trials.
#define CHUNK 1048576   // Size of block for reading ASCII files.
#define LEN_CONF_LINE   1024    // Maximum length of configuration line.
#define LEN_CONF_KEY    50      // Maximum length of configuration keyword.
#define LEN_CONF_VALUE  1024    // Maximum length of configuration keyword.
#define LEN_IN_LINE     256     // Maximum length of input line.
#define LEN_OUT_LINE    512     // Maximum length of output line.
#define DBL_TOL         1e-6    // Tolerance for comparison of coordinates.

#ifndef FLEN_FILENAME
#define FLEN_FILENAME   1025    // Maximum length of filename.
#endif
#ifndef FLEN_VALUE
#define FLEN_VALUE      71      // Maximum length of fits header value.
#endif

/******************************************************************************
  Definitions of mathematical/physical constants.
******************************************************************************/
#ifndef M_PI
#define M_PI            3.14159265358979323846
#endif

/******************************************************************************
  Definitions for configurations.
******************************************************************************/
#define DEFAULT_CONF_FILE "brickmask.conf"      // Default configuration file.
#define DEFAULT_FILE_TYPE 0     // Default type of the input file.
#define DEFAULT_COMMENT   '#'   // Default comment symbol for the input file.
#define DEFAULT_OVERWRITE 0     // Default behaviour for overwriting outputs.
#define DEFAULT_VERBOSE   1     // Default level of standard outputs.

/******************************************************************************
  Definitions for the format of outputs.
******************************************************************************/
#define FMT_WARN "\n\x1B[35;1mWarning:\x1B[0m "    // Magenta "Warning".
#define FMT_ERR  "\n\x1B[31;1mError:\x1B[0m "      // Red "Error".
#define FMT_EXIT "\x1B[31;1mExit:\x1B[0m "         // Red "Exit".
#define FMT_DONE "\r\x1B[70C[\x1B[32;1mDONE\x1B[0m]\n"    // Green "DONE".
#define FMT_FAIL "\r\x1B[70C[\x1B[31;1mFAIL\x1B[0m]\n"    // Red "FAIL".
#define FMT_KEY(key)    "\x1B[36;1m" #key "\x1B[0m"       // Cyan keyword.
#define OFMT_DBL "%.10g"                // Output format for double numbers.

/******************************************************************************
  Definitions for error codes.
******************************************************************************/
#define ERR_ARG         -1
#define ERR_MEM         -2
#define ERR_FILE        -3
#define ERR_INPUT       -4
#define ERR_RANGE       -5
#define ERR_STRING      -6
#define ERR_OTHER       -9

/******************************************************************************
  Definitions for small pieces of codes.
******************************************************************************/
#define P_ERR(...) fprintf(stderr, FMT_ERR __VA_ARGS__)
#define P_WRN(...) fprintf(stderr, FMT_WARN __VA_ARGS__)
#define P_EXT(...) fprintf(stderr, FMT_EXIT __VA_ARGS__)

#define FITS_EXIT {                     \
  P_EXT("cfitio error: ");              \
  fits_report_error(stderr, status);    \
  exit(status);                         \
}

#define MY_ALLOC(ptr,type,n,msg) {                              \
  (ptr) = (type *) malloc(sizeof(type) * (n));                  \
  if (!(ptr)) {                                                 \
    P_EXT("failed to allocate memory for " #msg ".\n");         \
    exit(ERR_MEM);                                              \
  }                                                             \
}

#define CHECKSTR(w,n,...) {             \
  if(w < 0 || w >= n) {                 \
    P_EXT(__VA_ARGS__);                 \
    exit(ERR_STRING);                   \
  }                                     \
}

/******************************************************************************
  Definitions for data types.
******************************************************************************/
typedef struct {                // Structure for reading mask bits.
  int d1;
  int d2;
  unsigned char *bit;
} MASK;

typedef struct {
  double crval[2];
  double crpix[2];
  double cd[2][2];
  double r[3][3];
  double cdtmp;
} WCS;

typedef struct {
  double ra;
  double dec;
  long idx;
  size_t oridx;
  char rest[LEN_IN_LINE];
  unsigned char mask;
  unsigned char flag;
} DATA;

#endif
