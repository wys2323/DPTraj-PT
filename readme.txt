1. Modify the parameters in the '. /data/parameters/' , 'parameters.py'
    - boundary.txt: Latitude and longitude range of the trajectory.
    - cellSize.txt: Divide the size of the grid.
    - neighborFile.txt: Record neighboring cells for each cell.
    - time.txt: Time horizon of the trajectory.
    - timeInterval.txt: Divide the interval of the time.

2. The '. /data/output/' folder is to store the data source files to be processed.
    - cellStay.txt: Record the stay time for each cell.
    We provided 5000 trajectories in '. /data/output/sample.txt'.

3. Generated synthetic trajectories are stored in the file directory  './data/output/syn'.