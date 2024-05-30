# NS-3 and SUMO LoRaWAN Mobility Performance: PDR and Delay Analysis 

> This project evaluates the mobility performance of LoRaWAN using NS-3 and SUMO simulations, focusing on Packet Delivery Ratio (PDR) and Delay. By simulating various mobility scenarios, we aim to understand how movement impacts the efficiency of LoRaWAN networks and provide insights for optimizing their performance in dynamic environments.

## Requirements

The minimum supported version of Ubuntu is `Ubuntu 18.04 LTS`. 
Firstly you may want update your system before proceeding, try running the following command.

```sh
sudo apt-get update
sudo apt-get upgrade
```

Install required packages:

```sh
#For NS-3 version 3.36 and later	
sudo apt-get install g++ python3 cmake ninja-build git
```

Install recommended packages:

```sh
sudo apt-get install ccache clang-format clang-tidy	gdb valgrind
```

The following packages are not required for our application. You may install any of them optionally if desired.

![img1](https://github.com/metehansozenli/NS-3_SUMO_Mobility_Project/blob/main/img/img1.png)

## Getting Started

We are now ready to proceed with the NS-3 installation.

## Installation of NS-3

Download a release tarball:

```sh
wget https://www.nsnam.org/releases/ns-allinone-3.41.tar.bz2
```

Extract the tarball and go into the build directory:

```sh
tar xfj ns-allinone-3.41.tar.bz2
cd ns-allinone-3.41/ns-3.41
```

Configure the default build profile:

```sh
./ns3 configure --enable-examples --enable-tests
```

Build the profile:

```sh
./ns3 build
```

Run unit tests to check the build:

```sh
./test.py
```

### We are ready to run a NS-3 simulation.
NOTE: You should run at /ns-3.41

```sh
./ns3 run first
```

After these steps, we can continue with the installation of the LoRaWAN module.

## LoRaWAN Module

### Requirements:

```sh
sudo apt install g++ python3 cmake ninja-build git ccache
```

Clone lorawan repository inside "src" directory: 

```sh
git clone https://github.com/signetlabdei/lorawan src/lorawan
```

Start the build process from scratch:

```sh
./ns3 clean
./ns3 configure --enable-tests --enable-examples --enable-modules lorawan
./ns3 build
```

Test the new build:

```sh
./test.py
```

### Running the LoRaWAN simple-example.

```sh
./ns3 run simple-network-example
```

We've completed all the necessary installations; now we can proceed with creating simulations using SUMO.

&nbsp;  &nbsp;  &nbsp;  

 # Creating Traffic Simulation with SUMO

Export the selected location from [OpenStreetMap](https://www.openstreetmap.org/#map=16/40.9870/29.037) to obtain a `.osm` file in the desired dimensions.

![img2](https://github.com/metehansozenli/NS-3_SUMO_Mobility_Project/blob/main/img/img2.jpeg)

### Convert an osm file to a Sumo network xml file:

```sh
netconvert --osm-files map.osm --output-file map.net.xml --geometry.remove --roundabouts.guess --ramps.guess --junctions.join --tls.guess-signals --tls.discard-simple --tls.join
```

| **Arguments** | **Description** |
| --- | --- |
| --osm-files | 'Specifies the input OSM file (map.osm)' |
| --output-file | 'Specifies the SUMO network file to be generated as output (map.net.xml).' |
| --geometry.remove | 'Simplifies the network by removing unnecessary geometric details.' |
| --roundabouts.guess | 'Automatically detects and creates roundabouts.' |
| --ramps.guess | 'Automatically detects and creates highway ramps.' |
| --junctions.join | 'Simplifies the network by joining nearby junctions.' |
| --tls.guess-signals | 'Estimates the locations of traffic lights.' |
| --tls.discard-simple | 'Discards simple traffic light configurations.' |
| --tls.join | 'Simplifies the network by joining nearby traffic lights.' |

### Generate random trips for vehicles within the specified xml:
NOTE: You should run at /ns-3.41

```sh
randomTrips.py -n map.net.xml -e 1000 -o map.trips.xml
```

| **Arguments** | **Description** |
| --- | --- |
| -n | 'Specifies the network file where trips will be generated (map.net.xml)' |
| -e | 'Sets the end time for trip generation process to 1000 seconds.' |
| -o | 'Specifies the output file where generated trips will be saved (map.trips.xml).' |

### Generate detailed route files for vehicles traveling on the network:

```sh
duarouter -n map.net.xml --route-files map.trips.xml -o map.rou.xml --ignore-errors"
```

| **Arguments** | **Description** |
| --- | --- |
| -n | 'Specifies the network file where routes will be generated (map.net.xml).' |
| --route-files map.trips.xml | 'Specifies the trip file (map.trips.xml) containing the generated trips.' |
| -o | 'Specifies the output file where generated routes will be saved (map.rou.xml).' |
| --ignore-errors | 'Ignores errors that occur during the route generation process.' |

```xml
<?xml version="1.0" encoding="iso-8859-1"?> 

<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.sf.net/xsd/sumoConfiguration.xsd"> 
<input>
    <net-file value="map.net.xml"/> 
    <route-files value="map.rou.xml"/> 
</input> 

<time> 
    <begin value="0"/> 
    <end value="6000"/>
</time>

</configuration>
```

## Contributors

* **Emir Karaman** - [EmirKaraman](https://github.com/Emir-Karaman)
* **Furkan Yaylaz** - [FurkanYaylaz](https://github.com/furkanyaylaz)
* **Metehan Sözenli** - [MetehanSözenli](https://github.com/metehansozenli)
