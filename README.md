# preconcentration_CE

[![Docker image](https://img.shields.io/badge/docker%20image-microfluidica%2Fpreconcentration--ce-0085a0)](https://hub.docker.com/r/microfluidica/preconcentration-ce/)

Application cases for preconcentration techniques described in the book chapter for running with [electroMicroTransport](https://gitlab.com/santiagomarquezd/electroMicroTransport).

## Docker usage

To run the application cases, you can use the Docker image [microfluidica/preconcentration-ce](https://hub.docker.com/r/microfluidica/preconcentration-ce/), which already includes an installation of electroMicroTransport.

To run the Docker image, you can use the following command (which will mount the current directory so that you can access your files from the container):

```bash
docker run --rm -it -v $PWD:/root -w /root microfluidica/preconcentration-ce
```

Or, if you use OpenFOAM's [`openfoam-docker` script](https://develop.openfoam.com/Development/openfoam/-/wikis/precompiled/docker):

```bash
openfoam-docker -image=microfluidica/preconcentration-ce
```

You will find the application cases inside the `$ELECTROMICROTRANSPORT_TUTORIALS/preconcentrationCE` directory.
