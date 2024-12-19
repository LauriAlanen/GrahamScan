from pathlib import Path
import math

X_INDEX = 0
Y_INDEX = 1

PLOT_HULL = 1
if PLOT_HULL:
    import matplotlib.pyplot as plt

class GrahamScan:
    def __init__(self):
        self.coordinates = []
        self.lowest_coordinate = math.inf
        self.convex_hull = []
        self.read_coordinate_file('graham.txt')
        self.compute_hull()
        self.print_hull()
            
    def read_coordinate_file(self, filename):
        p = Path(__file__).with_name(filename)
        with open(p, 'r') as coordinate_file:
            for line in coordinate_file:
                x, y = map(float, line.strip().split(' '))
                self.coordinates.append((x, y))
        
    def print_hull(self):
        for hull_coordinate in self.convex_hull:
            print(hull_coordinate)
    
    def plot_coordinates(self):
        if not self.convex_hull:
            print("No hull to plot.")
            return

        plt.scatter(
            [coord[X_INDEX] for coord in self.coordinates],
            [coord[Y_INDEX] for coord in self.coordinates],
            color="blue",
            label="Original Points"
        )

        hull_x = [coord[X_INDEX] for coord in self.convex_hull]
        hull_y = [coord[Y_INDEX] for coord in self.convex_hull]
        
        hull_x.append(self.convex_hull[0][X_INDEX])
        hull_y.append(self.convex_hull[0][Y_INDEX])
        
        plt.plot(hull_x, hull_y, color="red", label="Convex Hull", linewidth=2)

        plt.scatter(
            [self.lowest_coordinate[X_INDEX]],
            [self.lowest_coordinate[Y_INDEX]],
            color="green",
            label="Lowest Point (Start of Hull)",
            zorder=5
        )

        plt.title("Convex Hull and Original Points")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid(True)
        plt.legend()
        plt.show()
        
    def find_lowest_y_coordinate(self):
        lowest_coordinate = (math.inf, math.inf) # This the point P
        
        if not self.coordinates:
            print("No Coordinates Available!")
            return None
        
        for coordinate in self.coordinates:
            if coordinate[Y_INDEX] < lowest_coordinate[Y_INDEX]:
                lowest_coordinate = coordinate
                
            elif coordinate[Y_INDEX] == lowest_coordinate[Y_INDEX]:
                if coordinate[X_INDEX] < lowest_coordinate[X_INDEX]:
                    lowest_coordinate = coordinate
                
        self.lowest_coordinate = lowest_coordinate
        
    def sort_coordinates_by_angle(self): # Possible edge case unhandled (same polar angle)
        self.coordinates.sort(key = self.calculate_polar_angle)

    def calculate_polar_angle(self, coordinate): # Inspiration https://stackoverflow.com/questions/2676719/calculating-the-angle-between-a-line-and-the-x-axis
        delta_x = coordinate[X_INDEX] - self.lowest_coordinate[X_INDEX]
        delta_y = coordinate[Y_INDEX] - self.lowest_coordinate[Y_INDEX]
        polar_angle = math.atan2(delta_y, delta_x)
        return polar_angle  
        
    def calculate_cross_product(self, stack_second_top, stack_top, coordinate):
        cross_product = (
            (stack_top[X_INDEX] - stack_second_top[X_INDEX]) * (coordinate[Y_INDEX] - stack_second_top[Y_INDEX]) -
            (stack_top[Y_INDEX] - stack_second_top[Y_INDEX]) * (coordinate[X_INDEX] - stack_second_top[X_INDEX])
        )
    
        return cross_product

    def compute_hull(self): # This is the actual main logic behind graham scan. Is implemented following wikipedia algorithm steps
        self.find_lowest_y_coordinate()
        self.sort_coordinates_by_angle()
        if len(self.coordinates) < 3:
            print("Convex hull cannot be formed with less than 3 points.")
            return
        
        self.convex_hull.append(self.lowest_coordinate)
        for coordinate in self.coordinates:
            while len(self.convex_hull) > 1 and self.calculate_cross_product(self.convex_hull[-2], self.convex_hull[-1], coordinate) <= 0:
                self.convex_hull.pop()
            self.convex_hull.append(coordinate)
    
if __name__ == "__main__":
    hull = GrahamScan()
    if PLOT_HULL: hull.plot_coordinates()
