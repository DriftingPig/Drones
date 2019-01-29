#include "brickmask.h"

/******************************************************************************
Function `write_ascii`:
  Write the input galaxy data with the information of masks to the output.

Arguments:
  * `fname`:    the filename for the output;
  * `data`:     a pointer to the data to be saved;
  * `num`:      the number of galaxies;
  * `verbose`:  0 for concise outputs, 1 for detailed outputs.
Return:
  A non-zero integer if there is problem.
******************************************************************************/
int write_ascii(const char *fname, const DATA *data, const size_t num,
    const int verbose) {
  FILE *fp;
  int n, k;
  size_t i;
  char *buf, *end;
  char stmp[LEN_OUT_LINE];

  if (verbose) printf("\n  Filename : %s.\n", fname);

  if (!(fp = fopen(fname, "w"))) {
    P_ERR("cannot write to file `%s'.\n", fname);
    return ERR_FILE;
  }

  MY_ALLOC(buf, char, CHUNK, writing outputs);
  end = buf;

  /* Write file by chunks. */
  for (i = 0; i < num; i++) {
    n = snprintf(stmp, LEN_OUT_LINE, "%.12g %.12g %s %d %d\n", data[i].ra,
        data[i].dec, data[i].rest, data[i].mask, data[i].flag);
    CHECKSTR(n, LEN_OUT_LINE, "output line too long: %.12g %.12g %s %d %d\n"
        "Please enlarge LEN_OUT_LINE in `define.h`.\n", data[i].ra,
        data[i].dec, data[i].rest, data[i].mask, data[i].flag);

    if (end - buf + n < CHUNK) {        // there is still space in buf
      k = safe_strcpy(end, stmp, n + 1);
      CHECKSTR(k, n + 1, "unexpected error for writing: %s\n", stmp);
      end += k;
    }
    else {                              // write buf to file
      if (fwrite(buf, sizeof(char) * (end - buf), 1, fp) != 1) {
        P_ERR("failed to write to output: %s\n", stmp);
        return ERR_FILE;
      }
      k = safe_strcpy(buf, stmp, n + 1);
      CHECKSTR(k, n + 1, "unexpected error for writing: %s\n", stmp);
      end = buf + k;
    }
  }

  if ((n = end - buf) > 0) {
    if (fwrite(buf, sizeof(char) * n, 1, fp) != 1) {
      P_ERR("failed to write to output: %s\n", stmp);
      return ERR_FILE;
    }
  }

  fclose(fp);
  free(buf);
  return 0;
}


/******************************************************************************
Function `write_fits`:
  Append the mask and chunk information to the input galaxies, and write to a
  fits file.

Argument:
  * `input`:    filename of the input galaxy catalog;
  * `output`:   filename of the output file;
  * `data`:     a pointer to the data to be saved;
  * `num`:      the number of galaxies;
  * `verbose`:  0 for concise outputs, 1 for detailed outputs.
Return:
  A non-zero integer if there is problem.
******************************************************************************/
int write_fits(const char *input, const char *output, const DATA *data,
    const long num, const int verbose) {
  fitsfile *fin, *fptr;
  char fname[FLEN_FILENAME];
  int n, exist, col, status;
  long i;
  unsigned char *fitscol;
  char *ttype[2] = {"VETOMASK", "MCHUNK"};
  char *tform[2] = {"B", "B"};

  if (verbose) printf("\n  Filename: %s\n", output);

  status = 0;
  if (fits_file_exists(output, &exist, &status)) FITS_EXIT;
  if (exist > 0) n = snprintf(fname, FLEN_FILENAME, "!%s", output);
  else n = safe_strcpy(fname, output, FLEN_FILENAME);
  CHECKSTR(n, FLEN_FILENAME, "length of the output filename is too long.\n");

  status = 0;
  /* Copy input to output. */
  if (fits_open_data(&fin, input, READONLY, &status)) FITS_EXIT;
  if (fits_create_file(&fptr, fname, &status)) FITS_EXIT;
  if (fits_copy_file(fin, fptr, 1, 1, 1, &status)) FITS_EXIT;
  if (fits_close_file(fin, &status)) FITS_EXIT;

  /* Append columns to the output. */
  if (fits_get_num_cols(fptr, &col, &status)) FITS_EXIT;
  if (fits_insert_cols(fptr, col + 1, 2, ttype, tform, &status)) FITS_EXIT;

  MY_ALLOC(fitscol, unsigned char, num, the output column);

  /* Take into account the reordering of data */
  for (i = 0; i < num; i++) fitscol[data[i].oridx] = data[i].mask;
  if (fits_write_col(fptr, TBYTE, col + 1, 1, 1, num, fitscol, &status))
    FITS_EXIT;
  for (i = 0; i < num; i++) fitscol[data[i].oridx] = data[i].flag;
  if (fits_write_col(fptr, TBYTE, col + 2, 1, 1, num, fitscol, &status))
    FITS_EXIT;

  if (fits_close_file(fptr, &status)) FITS_EXIT;
  free(fitscol);
  return 0;
}

