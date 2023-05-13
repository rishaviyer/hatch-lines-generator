"""
Author: Iyer Rishav
U2223343D
Group: MA5
"""

import turtle
import math

global vertices
vertices = [(0, 0)]
global list_of_holes
list_of_holes = []
tolerance = 20
x_coordinate = 10000
y_coordinate = 10000


def DISTANCE(x1, y1, x2, y2):
    
    """
    Receives the coordinates of two points and returns the shortest
    distance (float) between them
    """
    
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def HATCHING_TOOL(Parameters, x, y_coor, Hatcher_Gradient_X, Hatcher_Gradient_Y):
    
    """
    Receives the line intersection parameters, x and y coordinates
    and slope of hatcher and draws the hatch lines inside the polygon
    """
    
    # Sort the list of Parameters in ascending order.
    Parameters.sort()
    
    # Set the pen color to red.
    turtle.pencolor("red")
    
    # Loop through the range of indices in Parameters.
    for i in range(len(Parameters)):
        
        # Check if the index is even (i.e., if the line should start).
        if i%2 == 0:
            
            # Lift the pen up.
            turtle.penup()
            
            # Move the turtle to the appropriate position using the given coordinates and gradient.
            turtle.goto(x + Parameters[i] * Hatcher_Gradient_X, y_coor + Parameters[i] * Hatcher_Gradient_Y)
        
        # Otherwise, the index is odd (i.e., if the line should end).
        else:
            
            # Put the pen down.
            turtle.pendown()
            
            # Draw the line by moving the turtle to the appropriate position using the given coordinates and gradient.
            turtle.goto(x + Parameters[i] * Hatcher_Gradient_X, y_coor + Parameters[i] * Hatcher_Gradient_Y)

def HATCH_LINE_INTERSECTIONS(points):
    
    Parameters = []
    epsilon_0 = 1e-15
    epsilon_1 = 1 + (1e-15)


    # coordinate in the second quadrant (top left of turtle screen) of the form (-x, y)
    x_coor = x_coordinate * (-1)                        
    y_coor = y_coordinate                     

    # Initializes the starting x - coordinate for checking if the previous and current coordinate are equal
    previous_x = x_coor   

    Hatcher_Gradient_X = math.cos((math.pi / 180) * angle)
    Hatcher_Gradient_Y = math.sin((math.pi / 180) * angle)

        
    for x in range(x_coor, x_coordinate + 1, spacing):

        for i in range(len(points) + 1):
            
            if i < len(points) - 1:
                
                Edge_Vertex_1_X = points[i][0]                         #x-coordinate of polygon edge vertex 1
                Edge_Vertex_1_Y = points[i][1]                         #y-coordinate of polygon edge vertex 1
                Edge_Vertex_2_X = points[i+1][0]                       #x-coordinate of polygon edge vertex 2
                Edge_Vertex_2_Y = points[i+1][1]                       #y-coordinate of polygon edge vertex 2
            Edge_Gradient_X = Edge_Vertex_2_X - Edge_Vertex_1_X          #gradient of polygon edge in x-direction
            Edge_Gradient_Y = Edge_Vertex_2_Y - Edge_Vertex_1_Y          #gradient of polygon edge in y-direction

            denominator = (Edge_Gradient_X
                            * Hatcher_Gradient_Y - Edge_Gradient_Y
                            * Hatcher_Gradient_X)
            if denominator != 0:

                #t1 = ((A2x * V2y – A2y * V2x) – (A1x * V2y – A1y * V2x)) / (V1x * V2y – V1y * V2x)
                Parameter_1 = ((x * Hatcher_Gradient_Y - y_coor
                                * Hatcher_Gradient_X) - (Edge_Vertex_1_X
                                * Hatcher_Gradient_Y - Edge_Vertex_1_Y
                                * Hatcher_Gradient_X))/ denominator 
            	

                #t2 = ((A2x * V1y – A2y * V1x) – (A1x * V1y – A1y * V1x)) / (V1x * V2y – V1y * V2x)
                Parameter_2 = ((x * Edge_Gradient_Y - y_coor
                                * Edge_Gradient_X) - (Edge_Vertex_1_X
                                * Edge_Gradient_Y - Edge_Vertex_1_Y
                                * Edge_Gradient_X)) / denominator

            # If the previous and current coordinates are not the same, calls the function for signalling the x - coordinate change
            if previous_x != x:
                HATCHING_TOOL(Parameters, previous_x, y_coor, Hatcher_Gradient_X, Hatcher_Gradient_Y)
                Parameters.clear()
                
            # If the first parameter lies between 0 and 1 (epsilon_0 is very close to 0 and epsilon_1 is very close to 1)
            #then it means hatch line intersects an edge
            if epsilon_0 <= Parameter_1 <= epsilon_1:
                Parameters.append(Parameter_2)
                previous_x = x
            

    

def IS_POINT_INSIDE_POLYGON(x, y):
    """
    Checks whether a point is inside a polygon and returns a boolean value to indicate so.
    """
    num_vertices = len(vertices)
    is_inside = False
    x1, y1 = vertices[0]  # Set the first vertex as the starting point for the loop
    
    # Loop through all the vertices of the polygon
    for i in range(num_vertices + 1):
        x2, y2 = vertices[i % num_vertices]  # The next vertex is the i+1th vertex, except when i=num_vertices
        
        # Check if the point is within the y bounds of the line segment
        if y > min(y1, y2):
            if y <= max(y1, y2):
                
                # Check if the point is to the left of the line segment
                if x <= max(x1, x2):
                    
                    # Calculate the x coordinate of the intersection between the point's y value and the line segment
                    if y1 != y2:
                        x_intersection = (y - y1) * (x2 - x1) / (y2 - y1) + x1
                    
                    # If the point is to the left of the intersection, it's inside the polygon
                    if x1 == x2 or x <= x_intersection:
                        is_inside = not is_inside
        
        x1, y1 = x2, y2  # Set the current vertex as the starting point for the next iteration of the loop
    
    return is_inside


def OFFSET_POLYGON():
    # Determine the centroid of the original polygon
    centroid_x = sum(vertex[0] for vertex in vertices) / len(vertices)
    centroid_y = sum(vertex[1] for vertex in vertices) / len(vertices)
    
    # Translate all the vertices of the original polygon so that the centroid is at the origin
    translated_vertices = [(vertex[0] - centroid_x, vertex[1] - centroid_y) for vertex in vertices]
    
    # Calculate the radius of the offset polygon
    radius = offset / math.sqrt(2)
    
    # Calculate the angle between each vertex of the original polygon and the positive x-axis
    angles = [math.atan2(vertex[1], vertex[0]) for vertex in translated_vertices]
    
    # Use the radius and the angle of each vertex to calculate the coordinates of the corresponding vertex in the offset polygon
    offset_vertices = [(radius * math.cos(angle), radius * math.sin(angle)) for angle in angles]
    
    # Translate all the vertices of the offset polygon so that the centroid of the original polygon is at its center
    translated_offset_vertices = [(vertex[0] + centroid_x, vertex[1] + centroid_y) for vertex in offset_vertices]
    
    # Find the corner vertices of the offset polygon by checking which vertices are closest to the corners of the original polygon
    corner_vertices = []
    for original_vertex in vertices:
        nearest_vertex = translated_offset_vertices[0]
        min_distance = math.dist(original_vertex, nearest_vertex)
        for offset_vertex in translated_offset_vertices[1:]:
            distance = math.dist(original_vertex, offset_vertex)
            if distance < min_distance:
                min_distance = distance
                nearest_vertex = offset_vertex
        corner_vertices.append(nearest_vertex)

    HATCH_LINE_INTERSECTIONS(corner_vertices)

def POLYGON_HOLE():
    
    # When the screen is clicked, call the DRAW_HOLE function.
    turtle.onscreenclick(DRAW_HOLE)

def DRAW_HOLE(x, y):
    
    # Check if the point (x, y) is inside the polygon using the IS_POINT_INSIDE_POLYGON function.
    if IS_POINT_INSIDE_POLYGON(x, y):
        
        # If the number of holes is 0, move the turtle to the point (x, y) and add it to the list of holes.
        if len(holes) == 0:
            turtle.penup()
            turtle.goto(x, y)
            holes.append((x, y))
        
        # Otherwise, draw a line from the previous point to the current point and add it to the list of holes.
        else:
            turtle.pendown()
            turtle.goto(x, y)
            holes.append((x, y))

            # Check if the user clicks on or near the first vertex, and if so, complete the polygon with a line segment.
            if len(vertices) >= 2 and DISTANCE(x, y, holes[0][0], holes[0][1]) <= tolerance:    
                turtle.goto(holes[0][0], holes[0][1])
                turtle.onscreenclick(None)
                list_of_holes.append(holes.copy())
                holes.clear()
                # If there are more holes to draw, call the POLYGON_HOLE function again.
                if len(list_of_holes) != hole_count:
                    
                    POLYGON_HOLE()
                else:
                    while True:
                        try:

                            # Creates a dialog box in turtle and prompts the user to enter 'Y' or 'N' (case insensitive) to determine if the vertices should be saved to a file.
                            save_to_file = turtle.textinput("Save?", "Do you want to save the polygon to a file? (Y/N or y/n)")

                            # If the user enters a valid input (i.e., 'Y' or 'N'), perform the appropriate action and break out of the loop.
                            if save_to_file and save_to_file.strip().lower() in ["y", "n"]:
                                if save_to_file.strip().lower() == "y":

                                    # Calls a function to save the vertices to a file named "vertices.txt".
                                    WRITE_TO_FILE_HOLES(list_of_holes)
                                    print("Vertices were saved to vertices.txt.")
                                else:
                                    print("Vertices were not saved to a file.")
                                break
                            else:

                                # If the user enters an invalid input, print an error message and repeat the loop.
                                raise ValueError("Invalid input. Please enter Y/N or y/n.")

                        except ValueError:

                            # If the user enters an invalid input, print an error message and repeat the loop.
                            print("Invalid input. Please enter Y/N or y/n.")
                        HATCH_LINE_INTERSECTIONS(vertices)
    
    
    
    

def POLYGON(x, y):

    """
    Allows the user to draw the polygon by click and uses DISTANCE()
    to check whether the user clicks on or near the first vertex. It
    also calls OUTPUT_FILE() (if the user wants to store the vertices
    in a file), FIND_CORNER_VERTICES() (if the user wants offset hatch
    lines) and POLYGON_HOLE() (if the user wants holes inside the polygon).
    """
    global holes
    holes = []
    
    # Adds the x and y coordinates as a tuple to a global list called vertices.
    vertices.append((x, y))
    
    # Moves the turtle to the x and y coordinates.
    turtle.goto(x, y)
    
    # Sets the turtle's speed to the maximum value.
    turtle.speed(0)
    
    # Checks if there are at least two vertices and if the distance between the current point and the first point is less than or equal to tolerance.
    if len(vertices) >= 2 and DISTANCE(x, y, vertices[0][0], vertices[0][1]) <= tolerance:
        
        # Moves the turtle to the first vertex.
        turtle.goto(vertices[0][0], vertices[0][1])

        
        # Disables click events for the turtle.
        turtle.onscreenclick(None)

        while True:
            try:

                # Creates a dialog box in turtle and prompts the user to enter 'Y' or 'N' (case insensitive) to determine if the vertices should be saved to a file.
                save_to_file = turtle.textinput("Save?", "Do you want to save the polygon to a file? (Y/N or y/n)")

                # If the user enters a valid input (i.e., 'Y' or 'N'), perform the appropriate action and break out of the loop.
                if save_to_file and save_to_file.strip().lower() in ["y", "n"]:
                    if save_to_file.strip().lower() == "y":

                        # Calls a function to save the vertices to a file named "vertices.txt".
                        WRITE_TO_FILE_POLYGON(vertices)
                        print("Vertices were saved to vertices.txt.")
                    else:
                        print("Vertices were not saved to a file.")
                    break
                else:

                    # If the user enters an invalid input, print an error message and repeat the loop.
                    raise ValueError("Invalid input. Please enter Y/N or y/n.")

            except ValueError:

                # If the user enters an invalid input, print an error message and repeat the loop.
                print("Invalid input. Please enter Y/N or y/n.")
            
        # If there are any holes, calls a function called POLYGON_HOLE for each hole.
        if hole_count > 0:
            print("You chose to draw ", hole_count, " holes. You can now draw holes inside the polygon on the turtle screen by clicking.")
            POLYGON_HOLE()
            
        # If there is an offset, calls a function called offset_polygon.
        elif offset > 0:
            OFFSET_POLYGON()
        
        # If there are no holes or offset, calls a function called HATCH_LINE_INTERSECTIONS with the vertices list as a parameter.
        else:
            HATCH_LINE_INTERSECTIONS(vertices)

def READ_FROM_FILE():
    """
    opens vertices.txt for reading (if it already exists) if the user choose file input method
    """

    polygons = []

    try:
        with open("vertices.txt", 'r') as read_file:
            polygon_lines = []

            for line in read_file:
                line = line.strip()

                # Ignore empty lines
                if not line:
                    continue

                # Check if the line starts with "Polygon:"
                if line.startswith('Polygon:'):
                    # If this is the start of a new polygon, add the previous one
                    if polygon_lines:
                        polygon = PARSE_POLYGON_LINE(polygon_lines)
                        polygons.append(polygon)
                        polygon_lines = []

                    # Add the current line to the list of lines for the new polygon
                    polygon_lines.append(line[len('Polygon:'):].strip())
                else:
                    # If the line doesn't start with "Polygon:", add it to the current polygon
                    polygon_lines.append(line)

            # Add the last polygon to the list
            if polygon_lines:
                polygon = PARSE_POLYGON_LINE(polygon_lines)
                polygons.append(polygon)

    except FileNotFoundError:
        print("Error: File not found.")
        return []

    except Exception as e:
        print("Error: {}".format(str(e)))
        return []

    return polygons


def PARSE_POLYGON_LINE(lines):
    """
    Removes all unnecessary characters, while retaining the vertices
    """
    # check if list is empty
    if not lines:
        raise ValueError("Empty list of lines")

    # get the first line and remove whitespace
    first_line = lines[0].strip()

    # check if the first line has a label and point list
    if ':' in first_line:
        
        # split the label and point list
        label, point_list = first_line.split(':')
        
        # replace any instances of "),(" with "), (" in the point list
        point_list = point_list.replace('),(', '), (')
    else:
        
        # if no label is provided, set it to an empty string
        label = 'Polygon'
        
        # replace any instances of "),(" with "), (" in the first line
        point_list = first_line.replace('),(', '), (')

    # create an empty list to store the points
    points = []
    
    # loop through each point string in the point list
    for point_str in point_list.split(', '):
        
        # remove the parentheses and any whitespace from the point string
        try:
            
            x, y = point_str.strip('()').split(',')
            
            # convert the x and y coordinates to floats and append them to the points list
            points.append((float(x), float(y)))
        except ValueError:
            print("Drawing Polygon")
            return []

    # return a list containing the label and the list of points
    return [label.strip(), points]


def WRITE_TO_FILE_POLYGON(vertices):
    
    """
    Write vertices to a file in the format "(x1,y1),(x2,y2),...,(xn,yn)\n".
    """
    
    # Open the "vertices.txt" file in "append" mode
    with open("vertices.txt", "a") as write_file:

        write_file.write("Polygon: ")
        
        # Loop through each vertex in the list of vertices
        for i in range(len(vertices)):
            
            # Write the coordinates of the vertex to the file in the format "(x,y)"
            write_file.write("({},{})".format(vertices[i][0], vertices[i][1]))
            
            # If the vertex is not the last vertex, add a comma to separate it from the next vertex
            if i < len(vertices) - 1:
                write_file.write(",")

        write_file.write(",({},{})".format(spacing, angle))   
        # Add a newline character at the end of the line of vertices
        write_file.write("\n")

def WRITE_TO_FILE_HOLES(holes_list):
    """
    Open holes.txt for appending and stores the vertices of the holes.
    """
    # Open the file "holes.txt" in append mode using the "with" statement in append mode
    with open("holes.txt", "a") as write_file:
        
        # Loop through each sublist in the "holes_list".
        for sublist in holes_list:
            
            # Write an opening square bracket to the file.
            write_file.write("[")
            
            # Loop through each tuple in the sublist.
            for i, tup in enumerate(sublist):
                
                # Write a tuple containing the vertex coordinates to the file.
                write_file.write("({},{})".format(tup[0], tup[1]))

                # If it's not the last tuple in the sublist, write a comma to separate it from the next one.
                if i < len(sublist) - 1:
                    write_file.write(",")
                    
            # Write a closing square bracket to the file to close the sublist.
            write_file.write("]")



def USER_INPUT():
    """
    requests and stores user input (input choice, hatch line parameters, holes) and sends the required parameters over to POLYGON() or INPUT_FILE()
    """
    
    # boolean variables for while loop to ask for user input
    invalid_input_1 = True
    invalid_input_2 = True
    invalid_input_3 = True
    invalid_input_4 = True
    
    
    global spacing
    global angle
    global offset
    global hole_count
    
    # loop to get a valid input for drawing mode
    while invalid_input_1:
        
        try:
            print("Do you want to draw the polygon using:\n1. Mouseclicks?\n2. File Input?\n(Enter 1 or 2.)")
            drawing_mode = int(input())
            
            # check if input is either 1 or 2, raise ValueError if not
            if drawing_mode not in [1, 2]:
                raise ValueError
            invalid_input_1 = False
        except ValueError:

            # prompt user to input again if the input is invalid
            print("Invalid input. Please enter either 1 or 2.")

    while invalid_input_2:
        try:
            hole_count = int(input("How many holes do you want inside the polygon (integer \u2265 0)? "))
            offset = int(input("Offset (a ratio) (integer \u2265 0): "))
            
            # check if input is non-negative, raise ValueError if not
            if hole_count < 0 and offset >= 0:
                raise ValueError
            invalid_input_2 = False
        except ValueError:

                # prompt user to input again if the input is invalid
                print("Invalid input. Please enter an integer greater than or equal to 0.")

    if drawing_mode == 1:
        # loop to get valid inputs for hatch lines' spacing, angle, and offset
        while invalid_input_3:
            try:
                print("Enter the spacing of the hatch lines and the angle that it makes with the x-axis.")
                spacing = int(input("Spacing (in pixels)(an integer > 0): "))
                angle = float(input("Angle (in degrees)(45 \u2264 \u0398 \u2264 135): "))

                # check if inputs satisfy the given constraints, raise ValueError if not
                if not (spacing > 0 and 45 <= angle <= 135):
                    raise ValueError
                invalid_input_3 = False
            except ValueError:

                # prompt user to input again if the input is invalid
                print("Invalid input. Please re-enter the values according to the instructions.")
            
        print("You can now create a polygon in the turtle window by clicking on points on the screen.")
    
        # Set up the turtle window and start listening for clicks
        display_screen = turtle.getscreen() # Get the turtle screen object
        pen = turtle.Screen() # Create a new turtle screen object
        turtle.setup(width=600, height=600) # Set the size of the turtle screen
        turtle.hideturtle() # Hide the turtle cursor
        pen.onclick(POLYGON) # Listen for clicks on the screen and call the polygon function
        pen.mainloop() # Start the main event loop for the turtle window
            
    else:
        # Ask the user which polygon to draw and get the vertices from a file
        while invalid_input_4:
            try:
                print("Which polygon do you want?\n1. Polygon 1\n2. Polygon 2\n3. Polygon 3\n(Enter 1, 2 or 3")
                polygon_from_file = int(input())
                if polygon_from_file not in [1,2,3]:
                    raise ValueError
                invalid_input_4 = False
            except ValueError:

                print("Invalid input. Please enter either 1, 2 or 3.")
                
        polygons = READ_FROM_FILE() # Call a function to get the vertices from a file
        try:
            vertices = polygons[polygon_from_file - 1][1][1:-1]
            vertices.insert(0, (0, 0))
            spacing = int(polygons[polygon_from_file - 1][1][-1][0])
            angle = polygons[polygon_from_file - 1][1][-1][1]
            # Move the turtle to each vertex and hide the cursor
            for vertex in vertices:
                turtle.hideturtle() # Hide the turtle cursor
                turtle.speed(0) # Set the turtle speed to 0 (fastest)
                turtle.goto(vertex[0], vertex[1]) # Move the turtle to the next vertex
            turtle.goto(vertices[0][0], vertices[0][1])

            if offset > 0:
                OFFSET_POLYGON()
            if hole_count > 0:
                POLYGON_HOLE()
        
            # Call a function to draw hatch lines on the polygon
            HATCH_LINE_INTERSECTIONS(vertices)
        except IndexError:
             print("Not enough polygons inside file. Restart the program and draw more or try lower polygon.")
    
        

# Calls the USER_INPUT() function to begin the program                            
USER_INPUT()        











    
    

    
    
        



                
        












    
        
            

                

    
    











 






    
