#!/bin/sh

# Copy table and executable to /replica
cp /model/Run/*.TBL .
cp /model/Run/wrf_hydro.exe .

# Uncomment to change # of jobs mpirun uses
echo 'localhost:'$1 > /etc/opt/hosts

# Update for user
echo "Setup complete, executing model"

# Execute wrf hydro
time mpirun ./wrf_hydro.exe 2>&1 > stdout_stderr.log

echo "Execution complete, cleaning up..."

# Cleanup
rm *.TBL wrf_hydro.exe
