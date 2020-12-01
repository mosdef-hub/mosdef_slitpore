FROM continuumio/miniconda3:4.8.2-alpine AS builder

ENV PATH /opt/conda/bin:$PATH

USER root

RUN apk update && apk upgrade && apk add bash cmake git git-lfs g++ gfortran make perl vim nano && \
	mkdir /software && \
	cd /software && \
    git clone https://github.com/rmatsum836/mosdef_slitpore && \
    cd mosdef_slitpore && \
    python setup.py install && cd ../ && \
	git clone https://github.com/GOMC-WSU/GOMC.git && \
	cd GOMC && chmod u+x metamake.sh && ./metamake.sh && cd ../ && \
    wget http://ftp.gromacs.org/pub/gromacs/gromacs-2020.3.tar.gz && \
	tar xzf gromacs-2020.3.tar.gz && cd gromacs-2020.3 && \
	mkdir build && cd build && \
	cmake .. -DGMX_BUILD_OWN_FFTW=ON -DREGRESSIONTEST_DOWNLOAD=OFF && \
	make && make check && make install && \
	echo "source /usr/local/gromacs/bin/GMXRC" >> /home/anaconda/.bashrc && \
	conda update conda -y && \
	. /opt/conda/etc/profile.d/conda.sh && \
    conda create --name slitpore lammps cp2k mosdef_cassandra foyer signac-flow matplotlib mdtraj \
    -c conda-forge -c mosdef -c omnia && \
	echo ". /opt/conda/etc/profile.d/conda.sh" >> /home/anaconda/.bashrc && \
	echo "conda activate base" >> /home/anaconda/.bashrc && \
	echo "conda activate slitpore" >> /home/anaconda/.bashrc && \
	conda activate slitpore && \
	conda clean -afy

ENV PATH /usr/local/gromacs/bin:/software/GOMC/bin:$PATH

WORKDIR /workspace

COPY entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh
RUN chown -R anaconda /workspace
RUN chmod 755 /workspace

USER anaconda

ENTRYPOINT ["/entrypoint.sh"]
CMD ["none"]
