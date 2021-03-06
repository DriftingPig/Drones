#include "load_conf.h"
#include "brickmask.h"
#ifdef OMP
#include <omp.h>
#endif

int main(int argc, char *argv[]) {
  fitsfile *fptr;
  int i, j, k, err, exist, status;
  size_t nbrick, ndata;
  long m, n, cnt;
  long *ubi;    // unique brick index
  unsigned char bit;
  char conf_file[FLEN_FILENAME], fname[FLEN_FILENAME], stmp[FLEN_FILENAME];
  char **brickname;
  const char *fnamefmt[NUMSUB] = SUB_FNAME;
  double x, y;
  double *ra1, *ra2, *dec1, *dec2;
  CONF conf;
  MASK maskbit;
  WCS wcs;
  DATA *data;

  /* Load configuration. */
  init_conf(&conf);
  n = safe_strcpy(conf_file, DEFAULT_CONF_FILE, FLEN_FILENAME);
  CHECKSTR(n, FLEN_FILENAME, "DEFAULT_CONF_FILE too long: %s\n"
      "Please adjust it in `define.h'.\n", DEFAULT_CONF_FILE);

  read_opt(argc, argv, conf_file, &conf);
  printf("Loading configuration ... ");
  fflush(stdout);

  read_conf(conf_file, &conf);
  if ((err = check_conf(&conf))) {
    printf(FMT_FAIL);
    P_EXT("please check your configuration.\n"
        "Try the -h option for more information.\n");
    return err;
  }
  if (conf.verbose) print_conf(conf_file, &conf);
  printf(FMT_DONE);

  /* Read the list of bricks. */
  printf("Reading the list of bricks ... ");
  fflush(stdout);
  status = exist = 0;

  if ((err = read_list(conf.list, &brickname, &ra1, &ra2, &dec1, &dec2,
      &nbrick, conf.verbose))) {
    printf(FMT_FAIL);
    P_EXT("failed to read the brick list.\n");
    return err;
  }

#ifdef OMP
#pragma omp parallel for
#endif
  for (n = 0; n < nbrick; n++) {        // Truncate boundary of bricks.
    ra1[n] = round(ra1[n] / DBL_TOL) * DBL_TOL;
    ra2[n] = round(ra2[n] / DBL_TOL) * DBL_TOL;
    dec1[n] = round(dec1[n] / DBL_TOL) * DBL_TOL;
    dec2[n] = round(dec2[n] / DBL_TOL) * DBL_TOL;
  }

#ifdef OMP
#pragma omp parallel for
#endif
  for (n = 1; n < nbrick; n++) {        // RA/Dec should be in increasing order.
    if (dec1[n] < dec1[n - 1]) {
      printf(FMT_FAIL);
      P_EXT("wrong Dec order in the brick list file.\n");
      exit(BAD_ORDER);
    }
    if (dec1[n] == dec1[n - 1] && ra1[n] < ra1[n - 1]) {
      printf(FMT_FAIL);
      P_EXT("wrong RA order in the brick list file.\n");
      exit(BAD_ORDER);
    }
  }
  printf(FMT_DONE);

  /* Read the input data file. */
  printf("Reading input data file ... ");
  fflush(stdout);

  if (conf.format == 0) {       // ASCII file
    if ((err = read_ascii(conf.input, conf.comment, &data, &ndata,
        conf.verbose))) {
      printf(FMT_FAIL);
      P_EXT("failed to read the input ASCII file.\n");
      return err;
    }
  }
  else if (conf.format == 1) {  // FITS file
    if ((err = read_fits(conf.input, &data, &ndata, conf.verbose))) {
      printf(FMT_FAIL);
      P_EXT("failed to read the input FITS file.\n");
      return err;
    }
  }

  /* Find bricks for data. */
  printf("Associating inputs with bricks ... ");
  fflush(stdout);

#ifdef OMP
#pragma omp parallel for
#endif
  for (n = 0; n < ndata; n++) {
    data[n].idx = find_brick(data[n].ra, data[n].dec, ra1, ra2, dec1, dec2,
        nbrick);
    if (data[n].idx < 0) {
      printf(FMT_FAIL);
      P_EXT("cannot find brick for the coordinate (%g, %g)\n",
          data[n].ra, data[n].dec);
      exit(ERR_RANGE);
    }
  }
  free(ra1);
  free(ra2);
  free(dec1);
  free(dec2);
  if (conf.verbose) printf("\n  Bricks assigned to all inputs successfully\n");

  /* Sort data by bricks and index unique bricks. */
  qsort(data, ndata, sizeof(DATA), compare_idx);

  cnt = 1;
  m = data[0].idx;
  for (n = 1; n < ndata; n++) {
    if (data[n].idx != m) {
      m = data[n].idx;
      cnt++;
    }
  }
  MY_ALLOC(ubi, long, cnt + 1, indexing inputs by bricks);

  ubi[0] = 0;
  ubi[cnt] = ndata;
  cnt = 1;
  m = data[0].idx;
  for (n = 1; n < ndata; n++) {
    if (data[n].idx != m) {
      m = data[n].idx;
      ubi[cnt] = n;
      cnt++;
    }
  }
  if (conf.verbose) printf("  Inputs indexed by bricks.\n");
  printf(FMT_DONE);

  /* Read and assign masks & flags. */
  printf("Reading and assigning masks ...");
  fflush(stdout);
  maskbit.d1 = maskbit.d2 = 0;
  maskbit.bit = NULL;

#ifdef OMP
#pragma omp parallel
  {
#pragma omp for firstprivate(exist,status,maskbit)  \
    private(i,j,k,n,stmp,fname,fptr,wcs,err,x,y,bit)
#endif
  for (m = 0; m < cnt; m++) {
    /* try all the possible filenames for bricks */
    for (i = 0; i < NUMSUB; i++) {
      n = snprintf(stmp, FLEN_FILENAME, fnamefmt[i],
          brickname[data[ubi[m]].idx]);
      CHECKSTR(n, FLEN_FILENAME, "brick filename too long.\n"
          "Please check SUB_FNAME in `define.h'.\n");
      n = snprintf(fname, FLEN_FILENAME, "%s/%s", conf.bdir, stmp);
      CHECKSTR(n, FLEN_FILENAME, "filename too long: %s/%s\n", conf.bdir, stmp);

      if (fits_file_exists(fname, &exist, &status)) FITS_EXIT;
      if (exist <= 0) continue; // omit non-existing files

      if (fits_open_data(&fptr, fname, READONLY, &status)) FITS_EXIT;
      if (fits_read_key(fptr, TINT, "NAXIS", &j, stmp, &status)) FITS_EXIT;
      if (j != 2) {
        P_ERR("wrong dimension in file: %s\n", fname);
        exit(BAD_NAXIS);
      }
      if (fits_read_key(fptr, TINT, "NAXIS1", &j, stmp, &status)) FITS_EXIT;
      if (fits_read_key(fptr, TINT, "NAXIS2", &k, stmp, &status)) FITS_EXIT;

      /* deal with coordinate convention keys */
      if ((err = read_wcs_header(fptr, &wcs))) {
        printf(FMT_FAIL);
        P_EXT("failed to read WCS keywords from the header: %s\n", fname);
        exit(err);
      }

      /* allocate memory for the mask bits if necessary */
      n = (long) j * k;
      if (maskbit.d1 * maskbit.d2 != j * k) {
        if (maskbit.bit) free(maskbit.bit);
        MY_ALLOC(maskbit.bit, unsigned char, n, bricks);
      }
      maskbit.d1 = j;
      maskbit.d2 = k;

      /* read brick */
      if (fits_read_tblbytes(fptr, 1, 1, n, maskbit.bit, &status)) FITS_EXIT;
      if (fits_close_file(fptr, &status)) FITS_EXIT;

      /* assign mask to data */
      for (n = ubi[m]; n < ubi[m + 1]; n++) {
        if ((err = wcs_world2pix(&wcs, data[n].ra, data[n].dec, &x, &y))) {
          printf(FMT_FAIL);
          P_EXT("failed to assign galaxies to bricks.\n");
          exit(err);
        }

        j = (int) round(x);
        k = (int) round(y);
        if (j < 0 || j >= maskbit.d1 || k < 0 || k >= maskbit.d2) {
          P_ERR("wrong pixel value (%d, %d) for coordinate (%g, %g)\n",
              j, k, data[n].ra, data[n].dec);
          exit(KEY_OUT_BOUNDS);
        }

        bit = maskbit.bit[j + (long) k * maskbit.d1];
        if (MASK_VALID) {
          if (XYBUG > 0 && (XYBUG_VALID)) data[n].mask += bit - XYBUG;
          else data[n].mask += bit;
          data[n].flag += (int) pow(2, i);

          if (XYBUG > 0) {
            j = (int) x;
            k = (int) y;
            if (j < 0 || j >= maskbit.d1 || k < 0 || k >= maskbit.d2) {
              P_ERR("wrong pixel value (%d, %d) for coordinate (%g, %g)\n",
                  j, k, data[n].ra, data[n].dec);
              exit(KEY_OUT_BOUNDS);
            }
            bit = maskbit.bit[j + (long) k * maskbit.d1];
            if (XYBUG_VALID) data[n].mask += XYBUG;
          }
        }
      }

    }
  }
  if (maskbit.bit != NULL) free(maskbit.bit);
#ifdef OMP
  }
#endif

  for (n = 0; n < nbrick; n++) {
    if (brickname[n] != NULL) free(brickname[n]);
  }
  free(brickname);
  free(ubi);
  printf(FMT_DONE);

  /* Save output. */
  printf("Saving output ...");
  fflush(stdout);

  if (conf.format == 0) {
    if ((err = write_ascii(conf.output, data, ndata, conf.verbose))) {
      printf(FMT_FAIL);
      P_EXT("failed to save results to the output ASCII file.\n");
      return err;
    }
  }
  else if (conf.format == 1) {
    if ((err = write_fits(conf.input, conf.output, data, ndata,
        conf.verbose))) {
      printf(FMT_FAIL);
      P_EXT("failed to save results to the output FITS file.\n");
      return err;
    }
  }
  printf(FMT_DONE);

  printf("Releasing memory ...");
  fflush(stdout);
  free(data);
  printf(FMT_DONE);

  return 0;
}

