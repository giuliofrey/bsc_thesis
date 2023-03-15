import os

#starting docker
print('Remember to start docker.')
#starting Open source routing machine from WLS
print('Starting OSRM')
os.system('wsl cd "/mnt/c/users/iodio/OneDrive - Università Commerciale Luigi Bocconi/Projects/mm/osrm"; '
          'docker run -t -i -p 5000:5000 -v "${PWD}:/data" ghcr.io/project-osrm/osrm-backend osrm-routed --algorithm mld /data/nord-ovest-latest.osrm')
