# Simple fNIRS Data Plotter

Simple solution to plot CSV blueberry data at a real time rate, running locally.

## HOWTO

Run the `plot.py` function like so:  

```
python3 plot.py -t 1613510000 -i blueberry_day_data_2021_02_16.csv
```
Where:  
`-t` is the start time (set as 0 to start at beginning of file)
`-i` is the input file CSV

## INSTALL

```
git clone <this repo location ssh or https>
cd <this repo>
python3 -m virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```


