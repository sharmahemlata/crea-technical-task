
# _CREA Technical Assignment_
-  [Assignment Description](https://energyandcleanair.notion.site/Technical-Assignment-Software-Engineer-314bdd68862b400d90f76ed445be46bd)
 
### Task 1: Help Rosa store files for her experiments

---
### Task 2: Collect Ozone mass mixing ratio at 850hPa

#### Prerequisites
- [Python3](https://www.python.org/downloads/)
- Copernicus UID and API KEY
	- Ensure that your Copernicus UID and API KEY are stored in  ~/.cdsapirc
	```bash
	cat ~/.cdsapirc
	url: https://cds.climate.copernicus.eu/api/v2
	key: <UID>:<API key>
	verify: 0
	```
#### Setup 
- Navigate to __task2__ directory
```bash
cd task2
```
-  create virtualenv crea_env
```bash
virtualenv crea_env
```
- Activate virtual environment
```bash
$ source crea_env/bin/activate
```
- Install Requirements 
```bash
pip install -r requirements.txt 
```
#### Build ozone_mass_mixing_ratio global raster
- To to build global raster (geotiff) of average Ozone mass mixing ratio at 850hPa of any given day run
```bash
python get_03_mass_mixing.py dd/mm/yyyy 
```
- Example: For 12th Jan 2020, run
```bash
python get_03_mass_mixing.py 12/01/2020 
```
- A geotiff file '__out.tiff__' will be produced alongside a png file '__out.png__'  in the task2 diretory
```bash
ls
crea_env  download.nc  get_03_mass_mixing.py  out.png  out.tiff  requirements.txt
```
---
### Task 3 [Option B]: Create a new trajectory dashboard

#### Prerequites 

- Navigate to trajectories dashboard
```bash
cd trajectories-dashboard
```
- Install dependencies
```bash
npm install
```
- Compile and Hot-Reload for Development
```bash
npm run  dev
```
-  Point your browser to http://localhost:8081. You should see the following dashboard
![Dashboard](images/dashboard.png)

- Please select City and Date from the dropdown menus. 
 
- If air trajectories for the chosen city on the chosen date are not available. You will see a 'Data not available' message. 

- If air trajectories are available, then you can see them as blue lines on the map. 
![Bangkok Results](images/bangkok.png)