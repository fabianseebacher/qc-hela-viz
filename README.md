# qc-hela-viz
 Dash app to visualize data from quality control HeLa samples in MS-based proteomics.
 
## Setup Instructions
1. Install Anaconda and create a new environment using the provided _requirements.txt_ file.
2. Activate the environment and startup the app from the command line using _python app.py_. Specify your ip and a port to provide access from other machines in your local network. Remember to allow connections through that port in your firewall whitelist.

Optional: 
If you want to deploy this in a production environment, e.g. on the web, use Gunicorn/Heroku. 

## Future features
* Set thresholds for red / yellow / green in a config file. 
 
## Screenshots
### Histogram view

![image](https://user-images.githubusercontent.com/71029831/121012880-76fa3e80-c798-11eb-9f16-c1d73f6f2afc.png)

### Dateplot view

![image](https://user-images.githubusercontent.com/71029831/121012959-9002ef80-c798-11eb-83d6-bfab1154c3e8.png)

