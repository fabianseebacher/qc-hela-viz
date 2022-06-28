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
![image](https://user-images.githubusercontent.com/71029831/176132016-2783243f-00eb-40ec-a306-df02ff877497.png)


### Explorer
![image](https://user-images.githubusercontent.com/71029831/176028611-d30e9526-30ea-479f-8419-aa0bf3c40948.png)





