#include <ctype.h>
#include "brickmask.h"

/******************************************************************************
Function `read_ascii`:
  Read the angular position of galaxies from an ASCII file. Each line of the
  file should be a record of a galaxy, with the leading 2 columns storing in
  `ra` and `dec`. The rest of the columns are stored in `rest`.

Arguments:
  * `fname`:    the filename of the input catalog;
  * `comment`:  comment symbol for the input catalog;
  * `data`:     a pointer to the array for storing input data;
  * `num`:      the number of galaxies read succesfully;
  * `verbose`:  0 for concise outputs, 1 for detailed outputs.
Return:
  A non-zero integer if there is problem.
******************************************************************************/
int read_ascii(const char *fname, const char comment, DATA **data, size_t *num,
    const int verbose) {
  FILE *fp;
  char *buf, *p, *end, *endl;;
  int i, j;
  size_t n, cnt, nrest;
  double ra, dec;

  if (verbose) {
    printf("\n  Filename: %s\n  Counting lines ...", fname);
    fflush(stdout);
  }

  if (!(fp = fopen(fname, "rb"))) {
    P_ERR("cannot open the " FMT_KEY(INPUT) ": %s\n", fname);
    return ERR_FILE;
  }

  n = 0;
  MY_ALLOC(buf, char, CHUNK, reading the file);

  while ((cnt = fread(buf, sizeof(char), CHUNK, fp))) {
    p = buf;
    end = p + cnt;
    while ((p = memchr(p, '\n', end - p))) {
      ++p;
      ++n;
    }
  }
  *num = n;

  if (verbose) {
    printf("\r  Number of records: %ld.\n  Allocating memory ... ", n);
    fflush(stdout);
  }

  MY_ALLOC(*data, DATA, n, the input data);
  memset(*data, 0, sizeof(DATA) * n);

  if (verbose) {
    cnt = sizeof(DATA) * n;
    printf("\r  ~ %.4g Mb memory allocated for the input data.\n"
        "  Reading ...  0%%", cnt / (1024.0 * 1024.0));
    fflush(stdout);
  }

  /* Read file by chunks. */
  fseek(fp, 0, SEEK_SET);
  n = nrest = 0;
  j = 0;
  while ((cnt = fread(buf + nrest, sizeof(char), CHUNK - nrest, fp))) {
    p = buf;
    end = p + nrest + cnt;
    if (cnt < CHUNK - nrest) *end = '\n';       // add '\n' to the last line
    while ((endl = memchr(p, '\n', end - p))) {
      *endl = '\0';     // replace '\n' by '\0' for processing lines
      while (isspace(p[0])) ++p;                // remove leading whitespaces
      if (p[0] == comment || p[0] == '\0') {    // comment or empty line
        p = endl + 1;
        continue;
      }

      if (sscanf(p, "%lf %lf %n", &ra, &dec, &i) != 2) {
        P_ERR("failed to read line: %s\n", p);
        return ERR_FILE;
      }

      cnt = safe_strcpy((*data)[n].rest, p + i, LEN_IN_LINE);
      CHECKSTR(cnt, LEN_IN_LINE, "line too long: %s\n"
          "Please adjust LEN_IN_LINE in `define.h'.", p);

      if (ra != 360) (*data)[n].ra = ra;
      else (*data)[n].ra = 0;
      (*data)[n].dec = dec;
      n++;
      p = endl + 1;
    }

    nrest = end - p;
    memmove(buf, p, nrest);

    if (verbose) {
      i = (int) (n * 20 / (*num));
      if (i != j) {
        j++;
        printf("\b\b\b\b%3d%%", j * 5);
        fflush(stdout);
      }
    }
  }

  *num = n;
  fclose(fp);
  free(buf);
  if (verbose) printf("\r  %ld valid objects recorded.\n", n);

  return 0;
}


/******************************************************************************
Function `read_fits`:
  Read the angular position of galaxies from a fits file.

Arguments:
  * `fname`:    the filename of the input catalog;
  * `data`:     a pointer to the array for storing input data;
  * `num`:      the number of galaxies read succesfully;
  * `verbose`:  0 for concise outputs, 1 for detailed outputs.
Return:
  A non-zero integer if there is problem.
******************************************************************************/
int read_fits(const char *fname, DATA **data, size_t *num, const int verbose) {
  fitsfile *fptr;
  int col, status;
  long i, n;
  double *fitscol;

  if (verbose) printf("\n  Filename: %s\n", fname);

  status = 0;
  if (fits_open_data(&fptr, fname, READONLY, &status)) FITS_EXIT;
  if (fits_get_num_rows(fptr, &n, &status)) FITS_EXIT;
  if (verbose) {
    printf("\r  Number of records: %ld.\n  Allocating memory ... ", n);
    fflush(stdout);
  }

  MY_ALLOC(fitscol, double, n, the column of input data);
  MY_ALLOC(*data, DATA, n, the input data);
  memset(*data, 0, sizeof(DATA) * n);

  if (verbose) printf("\r  ~ %.4g Mb memory allocated for the input data.\n",
      sizeof(DATA) * n / (1024.0 * 1024.0));

  if (fits_get_colnum(fptr, CASEINSEN, "RA", &col, &status)) FITS_EXIT;
  if (fits_read_col_dbl(fptr, col, 1, 1, n, 0, fitscol, 0, &status)) FITS_EXIT;
  for (i = 0; i < n; i++) (*data)[i].ra = fitscol[i];

  if (fits_get_colnum(fptr, CASEINSEN, "DEC", &col, &status)) FITS_EXIT;
  if (fits_read_col_dbl(fptr, col, 1, 1, n, 0, fitscol, 0, &status)) FITS_EXIT;
  for (i = 0; i < n; i++) (*data)[i].dec = fitscol[i];

  if (fits_close_file(fptr, &status)) FITS_EXIT;
  free(fitscol);

  for (i = 0; i < n; i++) (*data)[i].oridx = i;
  *num = n;
  return 0;
}


/******************************************************************************
Function `read_list`:
  Read the brick name and range of (RA, Dec) from a brick list file.

Arguments:
  * `fname`:    the filename of the brick list;
  * `bname`:    a pointer to the array for storing brick names;
  * `ra1`:      a pointer to the array for storing lower limit of ra;
  * `ra2`:      a pointer to the array for storing upper limit of ra;
  * `dec1`:     a pointer to the array for storing lower limit of dec;
  * `dec2`:     a pointer to the array for storing upper limit of dec;
  * `num`:      the number of bricks;
  * `verbose`:  0 for concise outputs, 1 for detailed outputs.
Return:
  A non-zero integer if there is problem.
******************************************************************************/
int read_list(const char *fname, char ***bname, double **ra1, double **ra2,
    double **dec1, double **dec2, size_t *num, const int verbose) {
  fitsfile *fptr;
  int width, col, status;
  long i, n;

  if (verbose) printf("\n  Filename: %s\n", fname);
  status = 0;
  if (fits_open_data(&fptr, fname, READONLY, &status)) FITS_EXIT;
  if (fits_get_num_rows(fptr, &n, &status)) FITS_EXIT;
  if (verbose) {
    printf("\r  Number of bricks: %ld.\n  Allocating memory ... ", n);
    fflush(stdout);
  }

  MY_ALLOC(*ra1, double, n, lower limit of RA);
  MY_ALLOC(*ra2, double, n, upper limit of RA);
  MY_ALLOC(*dec1, double, n, lower limit of Dec);
  MY_ALLOC(*dec2, double, n, upper limit of Dec);
  MY_ALLOC(*bname, char *, n, name of bricks);

  /* Get width of the field BRICKNAME. */
  if (fits_get_colnum(fptr, CASEINSEN, "BRICKNAME", &col, &status)) FITS_EXIT;
  if (fits_get_col_display_width(fptr, col, &width, &status)) FITS_EXIT;
  for (i = 0; i < n; i++)
    MY_ALLOC((*bname)[i], char, width + 1, name of bricks);

  if (verbose) {
    i = sizeof(double) * n * 4 + sizeof(char *) * n;
    i += sizeof(char) * n * (width + 1);
    printf("\r  ~ %.4g Mb memory allocated for the list of bricks.\n",
        i / (1024.0 * 1024.0));
  }

  /* Read brickname. */
  if (fits_read_col_str(fptr, col, 1, 1, n, "", *bname, 0, &status)) FITS_EXIT;

  if (fits_get_colnum(fptr, CASEINSEN, "RA1", &col, &status)) FITS_EXIT;
  if (fits_read_col_dbl(fptr, col, 1, 1, n, 0, *ra1, 0, &status)) FITS_EXIT;
  if (fits_get_colnum(fptr, CASEINSEN, "RA2", &col, &status)) FITS_EXIT;
  if (fits_read_col_dbl(fptr, col, 1, 1, n, 0, *ra2, 0, &status)) FITS_EXIT;
  if (fits_get_colnum(fptr, CASEINSEN, "DEC1", &col, &status)) FITS_EXIT;
  if (fits_read_col_dbl(fptr, col, 1, 1, n, 0, *dec1, 0, &status)) FITS_EXIT;
  if (fits_get_colnum(fptr, CASEINSEN, "DEC2", &col, &status)) FITS_EXIT;
  if (fits_read_col_dbl(fptr, col, 1, 1, n, 0, *dec2, 0, &status)) FITS_EXIT;

  if (fits_close_file(fptr, &status)) FITS_EXIT;
  *num = n;
  return 0;
}


/******************************************************************************
Function `read_wcs_header`:
  Read the header of a fits file for WCS convention.

Arguments:
  * `fptr`:     a pointer to the opened fits file;
  * `wcs`:      a pointer to the structure for storing WCS information.
Return:
  A non-zero integer if there is problem.
******************************************************************************/
int read_wcs_header(fitsfile *fptr, WCS *wcs) {
  int i, status = 0;
  char stmp[FLEN_FILENAME], value[FLEN_VALUE];
  double alpha[2], sina[2], cosa[2];

  if (fits_read_key(fptr, TSTRING, "CTYPE1", value, stmp, &status)) FITS_EXIT;
  if (strncmp(value, "RA---TAN", 9)) {
    P_ERR("only CTYPE1='RA---TAN' is supported.\n");
    return BAD_KEYCHAR;
  }
  if (fits_read_key(fptr, TSTRING, "CTYPE2", value, stmp, &status)) FITS_EXIT;
  if (strncmp(value, "DEC--TAN", 9)) {
    P_ERR("only CTYPE2='DEC--TAN' is supported.\n");
    return BAD_KEYCHAR;
  }

  /* Quit for unsupported WCS convention. */
  fits_read_key_str(fptr, "DISTORT", value, stmp, &status);
  if (status != KEY_NO_EXIST) {
    P_ERR("WCS convention with DISTORT is not supported\n");
    return WCS_ERROR;
  }
  status = 0;
  fits_read_key_str(fptr, "REVERSE", value, stmp, &status);
  if (status != KEY_NO_EXIST) {
    P_ERR("WCS convention with REVERSE is not supported\n");
    return WCS_ERROR;
  }
  status = 0;
  fits_read_key_str(fptr, "LONGPOLE", value, stmp, &status);
  if (status != KEY_NO_EXIST) {
    P_ERR("WCS convention with LONGPOLE is not supported\n");
    return WCS_ERROR;
  }
  status = 0;
  fits_read_key_str(fptr, "PVF1", value, stmp, &status);
  if (status != KEY_NO_EXIST) {
    P_ERR("WCS convention with PVF1 is not supported\n");
    return WCS_ERROR;
  }
  status = 0;

  /* Read coordinate convention keys. */
  if (fits_read_key(fptr, TDOUBLE, "CRVAL1", &(wcs->crval[0]), stmp, &status))
    FITS_EXIT;
  if (fits_read_key(fptr, TDOUBLE, "CRVAL2", &(wcs->crval[1]), stmp, &status))
    FITS_EXIT;
  if (fits_read_key(fptr, TDOUBLE, "CRPIX1", &(wcs->crpix[0]), stmp, &status))
    FITS_EXIT;
  if (fits_read_key(fptr, TDOUBLE, "CRPIX2", &(wcs->crpix[1]), stmp, &status))
    FITS_EXIT;
  if (fits_read_key(fptr, TDOUBLE, "CD1_1", &(wcs->cd[0][0]), stmp, &status))
    FITS_EXIT;
  if (fits_read_key(fptr, TDOUBLE, "CD1_2", &(wcs->cd[0][1]), stmp, &status))
    FITS_EXIT;
  if (fits_read_key(fptr, TDOUBLE, "CD2_1", &(wcs->cd[1][0]), stmp, &status))
    FITS_EXIT;
  if (fits_read_key(fptr, TDOUBLE, "CD2_2", &(wcs->cd[1][1]), stmp, &status))
    FITS_EXIT;

  /* Get prepared for WCS convention. */
  for (i = 0; i < 2; i++) {
    alpha[i] = wcs->crval[i] * M_PI / 180.0;
    sina[i] = (wcs->crval[i] == 0 || wcs->crval[i] == 180) ? 0 : sin(alpha[i]);
    cosa[i] = (wcs->crval[i] == -90 || wcs->crval[i] == 90) ? 0 : cos(alpha[i]);
  }
  wcs->r[0][0] = cosa[0] * sina[1];
  wcs->r[0][1] = sina[0] * sina[1];
  wcs->r[0][2] = -cosa[1];
  wcs->r[1][0] = -sina[0];
  wcs->r[1][1] = cosa[0];
  wcs->r[1][2] = 0;
  wcs->r[2][0] = cosa[0] * cosa[1];
  wcs->r[2][1] = sina[0] * cosa[1];
  wcs->r[2][2] = sina[1];

  wcs->cdtmp = wcs->cd[0][0] * wcs->cd[1][1] - wcs->cd[0][1] * wcs->cd[1][0];
  if (wcs->cdtmp == 0) {
    P_ERR("the CD matrix is not reversible.\n");
    return WCS_ERROR;
  }

  return 0;
}

