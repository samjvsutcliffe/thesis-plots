rm -r data*
rsync --progress -az --exclude=mpi-worker rmvn14@hamilton8.dur.ac.uk:"~/glacier/thesis/ice-cliff-slip/data-cliff-stability/" ./data-slip
rsync --progress -az --exclude=mpi-worker rmvn14@hamilton8.dur.ac.uk:"~/glacier/thesis/ice-cliff-noslip/data-cliff-stability/" ./data-noslip
rsync --progress -az --exclude=mpi-worker rmvn14@hamilton8.dur.ac.uk:"~/glacier/thesis/ham-thesis-ice-cliff-stability/data-cliff-stability/" ./data-frictional
