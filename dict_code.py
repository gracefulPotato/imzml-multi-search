import sys
from pyimzml.ImzMLParser import ImzMLParser
import tkinter
import pandas
import json

# Example usage:
# python dict_code.py imzML\ files/CRP\ titration/230717_beads_tritration.imzML

args = sys.argv[1:]
if len(args) != 1:
	print("Usage: python pyimzml\ code.py path/to/<file>.imzml")
	exit(0)
	
filename = args[0]

p = ImzMLParser(filename)
my_spectra = []
all_intensities = []
for idx, (x,y,z) in enumerate(p.coordinates):
    mzs, intensities = p.getspectrum(idx)
    all_intensities.extend(intensities)
    my_spectra.append([mzs, intensities, (x, y, z)])
print(my_spectra[0])
print(len(my_spectra))
average_intensity = sum(all_intensities)/len(all_intensities)
print("Average abundance: "+str(average_intensity))

stop=False

while(stop==False):
	abundance_threshold = float(input("Enter abundance threshold: "))
	# Create dictionary mapping rounded masses to coordinates
	mass_dict = {}
	for coordinate in my_spectra:
		for index in range(len(coordinate[0])):
			if abundance_threshold < float(coordinate[1][index]):
				rounded_mz = str(round(coordinate[0][index], 1))
				mass_entry = [str(coordinate[0][index]),str(coordinate[1][index]),str(coordinate[2])]
				if rounded_mz in mass_dict:
					mass_dict[rounded_mz].append(mass_entry)
				else:
					mass_dict[rounded_mz] = [mass_entry]
	out_file = open("mass_dict.json", "w")
	json_string = json.dumps(mass_dict)
	json.dump(json_string, out_file)
	out_file.close()
	print("done")

	rerun = input("Would you like to rerun with a lower abundance threshold? yes or no: ")
	if rerun == "no":
		stop=True
	


#print("Canvas width is " + canvas_width)
		
# For a list of target masses (import from a excel file)
# find approximate match of mass within 0.5
# use corresponding index to identify abundance threshold
# find relatively higher abundance
# first export into a readable data structure ()
# Make an image with x,y coordinates brightened up
# (tkinter?)


# divide coordinates by 2 to make window smaller than monitor
# draw a rectangle in middle of window and have all points in there
# so that could have titles/labels outside of that
# ideally it would read out the percentage of coverage in that area
# color heatmap? or size of circle could be how many in that area
# or use existing biostatistics tool to display?
# or display summary label in an area that has more than 10 dots
# if dots are within x pixels then draw a bigger dot


