#!/usr/bin/env python3.2

# Ali Clarke
# Practical Problem Solving
# Coursework 2
# Created 19/11/12
# Modified 27/11/12

import json, requests, sys, webbrowser, os

#Argument Validation
#Checks for the presence of two additional arguments 
try:
    detail = sys.argv[1]
    period = sys.argv[2]
except:
    sys.exit('Usage: ./quakes.py <detail> <period>')

#Argument content validation 
if sys.argv[1] == '2.5':
        valid=True
       
elif sys.argv[1] == '4.5':
        valid=True
elif sys.argv[1] == 'significant':
        valid=True
else:
        sys.exit('invalid command')
       
if sys.argv[2] == "week":
        valid=True
       
elif sys.argv[2] == "month":
        valid=True
       
else:
        sys.exit('''
Usage: ./quakes.py <detail> <period>
Valid Commands are:
	Detail:				Period:
	2.5					week
	4.5					month
	significant

''')
 
#Begin Functions
def write(data):
	
        out_file = open('test.loc', 'wt')
        for value in data:
                out_file.write(str(value) + "\n")
        out_file.close()

def mean(data):
	mean = (sum(data)/float(len(data)))
	return mean

def genhtml(dyndata):
	out_file = open('quakes-level-period.html', 'wt')
		
	header = '''
				<html>
				  <head>
				<title> Earthquake Plots </title>
				    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
				    <script type="text/javascript">
				      google.load("visualization", "1", {packages:["map"]});
				      google.setOnLoadCallback(drawMap);
				      function drawMap() {
				        var data = google.visualization.arrayToDataTable([
						[\'Lat\', \'Lon\', \'Name\'],
				'''

		
	end = '''
						       ]);

								        var map = new google.visualization.Map(document.getElementById('map_div'));
								        map.draw(data, {showTip: true});
								      }
								    </script>
								  </head>

								  <body>
								    <div id="map_div" style="width: 800px; height: 500px"></div>
								  </body>
								</html>					'''
		
		
	out_file.write(header)
	
	#loop to write each quake into the map
	for value in dyndata:
		#print(value)
		out_file.write(value)
		
	out_file.write(end)
	
	#closes the file to avoid corruption
	out_file.close()
	
	#gets the location of the html file and assigns it to a variable so that it can be displayed in a browser
	map = 'file://' + os.path.realpath('quakes-level-period.html')
	webbrowser.open(map)
#end functions

url = 'http://earthquake.usgs.gov/earthquakes/feed/geojson/'+ detail + '/'+ period
#print(url) #debugging url print, to make sure string is concatinated properly

#apply error caching the whole section that requires a network connection
#ensures that an informative message is displayed incase of lack of connection
try:
	response = requests.get(url) #load data
	data = json.loads(response.text)

	quakes = data['features']
 
	#initalize lists for parsed data storage
	mag=[]
	depth=[]
	xy=[] 
	x=[]
	y=[]
	
	dyndata=[]
	template = '{:f}, {:f}'

 
	for quake in quakes:
 			#writes each data set into their own lists
			spec = (quake['geometry']['coordinates'])
			xy.append(str(str(spec[1])) + ', ' + str(spec[0]))
			x.append(str(spec[1]))
			y.append(str(spec[0]))
			
			mag.append(quake['properties']['mag'])
			depth.append(spec[2])
			
			
			place = (quake['properties']['place'])
			place = place.replace("'", "") #strips out the ' in the description of places
			
			#creates the correctly formatted infomation for the g.maps vis api
			dyndata.append('[' + str(str(spec[1])) + ', ' + str(spec[0]) + ', \'' + place + '\'],')
		
 	
 
	template2 = 'Mean Magnitude: {:f}, Mean Depth: {:f}'
	
	#call functions
	write(data= xy)
	genhtml(dyndata)
	
	print(template2.format(mean(mag), mean(depth)))

except:
	sys.exit("No Network Connection") #incase of network error




