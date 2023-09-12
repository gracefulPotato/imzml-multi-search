import sys
from pyimzml.ImzMLParser import ImzMLParser
import tkinter
import pandas
import json

# Example usage:
# python pyimzml\ code.py imzML\ files/CRP\ titration/230717_beads_tritration.imzML

args = sys.argv[1:]
if len(args) < 2:
	print("Usage: python pyimzml\ code.py path/to/<file>.imzml path/to/<mass_list>.xlsx")
	exit(0)
	
filename = args[0]
mass_list_file = args[1]



p = ImzMLParser(filename)
my_spectra = []
for idx, (x,y,z) in enumerate(p.coordinates):
    mzs, intensities = p.getspectrum(idx)
    my_spectra.append([mzs, intensities, (x, y, z)])
print(my_spectra[0])
print(len(my_spectra))


with open('mass_dict.json') as json_file:
	mass_dict = json.load(json_file)
	mass_dict = json.loads(mass_dict)
#	mass_dict = mass_dict.to_dict()

# search the x,y for other masses in target_masses
# Read target masses from excel file
massDf = pandas.read_excel(mass_list_file)
print(massDf)
target_excel_masses = massDf["[M+Na]+"].to_list()
# Select first mass from excel
first_mass = massDf["[M+Na]+"][0]
print("first:"+str(first_mass))


rounded_target_mass = str(round(first_mass,1))
hot_spots = []
mass_total = 0
'''if rounded_target_mass in mass_dict:
	print(mass_dict[rounded_target_mass])
	for mass_coordinate in mass_dict[rounded_target_mass]:
		if mass_coordinate[1] >= 5000:
			hot_spots.append(coordinate[2]) 
print(hot_spots)'''
#select the x,y,z located by the hotspots	
target_excel_masses = massDf["[M+Na]+"].to_list()
for target_mass in target_excel_masses:
	for i in [-0.1,0,0.1]:
		rounded_target_mass = str(round(target_mass,1)+i)
		if rounded_target_mass in mass_dict:
			print("in dict: "+str(rounded_target_mass))
			mass_entry = mass_dict[rounded_target_mass]
			for entry in mass_entry:
				coords = entry[2][1:-1]
				(x,y,z) = coords.split(",")
				hot_spots.append([int(x),int(y),entry[0]])
				mass_total += float(entry[0])
			break
		else:
			print("not in dict: "+str(rounded_target_mass))
print(hot_spots)
print(len(hot_spots))
average_mz = mass_total/len(hot_spots)
#unique_hot_spots = set(hot_spots)
#print(len(unique_hot_spots))
#f = open("mass_dict_keys","w")
#f.write(mass_dict.keys().to_list())	




root = tkinter.Tk()

frame= tkinter.Frame(root)
frame.pack()  # pack the frame
canvas = tkinter.Canvas(frame, width=2064,height=2064, borderwidth=0)
canvas.grid(row=0, column=0)

def create_circle(canvas, x, y, radius, color="black"):
    return canvas.create_oval(x,y,x+radius,y+radius,fill=color, outline="")
    
    
coord_dict = {}
for spot in hot_spots:
	if (spot[0], spot[1]) not in coord_dict:
		coord_dict[(spot[0], spot[1])] = [spot[2]]
	else:
		coord_dict[(spot[0], spot[1])].append(spot[2])
		
print(coord_dict)
max_len = 0
for i in coord_dict:
	print(len(coord_dict[i]))
	if len(coord_dict[i]) > max_len:
		max_len = len(coord_dict[i])
print("max_len: " + str(max_len))



#canvas.create_rectangle(x,y,x+1,y+1,fill="purple")
for coordinate in hot_spots:
	#coordinate[1] = coordinate[1][1:-1]
	#(x,y,z) = coordinate[1].split(",")
	if float(coordinate[2]) >= average_mz:
		color = "red"
	else:
		color = "blue"
	create_circle(canvas, coordinate[0], coordinate[1],2,color)
	
for i in coord_dict:
	if len(coord_dict[i]) > max_len-5:
		create_circle(canvas, i[0], i[1],15,"green1")
		label_text = "("+str(i[0])+", "+str(i[1])+"): "+str(len(coord_dict[i]))+" sequences"
		text_1 = tkinter.Label(text=label_text, bg='white', font=("Ariel", 12), fg='black')
		text_1.place(x=i[0]+10, y=i[1]+10)
#text_2 = tkinter.Label(text="French", bg='white', font=("Ariel", 12), fg='black')
#text_2.place(x=200, y=100)
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

#


# User input example:
#canvas_width = input("Enter canvas width: ")
#print("Canvas width is " + canvas_width)
#canvas_height = input("Enter canvas height: ")
#print("Canvas height is " + canvas_height)


root.mainloop()  # keep the GUI open


