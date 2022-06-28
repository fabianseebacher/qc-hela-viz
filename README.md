# qc-hela-viz
 Dash app to visualize data from quality control HeLa samples in MS-based proteomics.
 
## Setup Instructions
1. Install Anaconda and create a new environment using the provided _requirements.txt_ file.
2. Activate the environment and startup the app from the command line using _python app.py_. Specify your ip and a port to provide access from other machines in your local network. Remember to allow connections through that port in your firewall whitelist.

Optional: 
If you want to deploy in a production environment, e.g. on the web, use Gunicorn/Heroku. 

## Known issues
* Dateplots do not always resize correctly. Resizing the window and then maximizing again usually works as a workaround.

## Future features
* Set thresholds for red / yellow / green in a config file. 
 
## Screenshots

### Live View
![image](https://user-images.githubusercontent.com/71029831/176133207-1d714ec5-095e-4d4c-96fb-c928b3049547.png)


### Explorer
![image](https://user-images.githubusercontent.com/71029831/176133608-7ecf01d8-c6c9-4f81-9556-264ee1eb1427.png)





