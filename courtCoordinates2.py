import pandas as pd 
import numpy as np 

class CourtCoordinates:
    '''
    Stores court dimensions and calculates the (x,y,z) coordinates of the outside perimeter, 
    three point line, backboard, and hoop.
    The default dimensions of a men's ncaa court according to https://modutile.com/basketball-half-court-dimensions/#
    '''
    def __init__(self):
        self.court_length = 120                 # the court is 94 feet long
        self.court_width = 53.3                  # the court is 50 feet wide
        

    @staticmethod
    def calculate_quadratic_values(a, b, c):
        '''
        Given values a, b, and c,
        the function returns the output of the quadratic formula
        '''
        x1 = (-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)
        x2 = (-b - (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)

        return x1, x2

    def __get_court_perimeter_coordinates(self):
        '''
        Returns coordinates of full court perimeter lines. A court that is 50 feet wide and 94 feet long
        In shot chart data, each foot is represented by 10 units.
        '''
        width = self.court_width
        length = self.court_length
        court_perimeter_bounds = [
            [0, 0, 0], 
            [width, 0, 0], 
            [width, length, 0], 
            [0, length, 0], 
            [0, 0, 0]
        ]

        court_df = pd.DataFrame(court_perimeter_bounds, columns=['x','y','z'])
        court_df['line_group'] = 'outside_perimeter'
        court_df['color'] = 'court'
        
        return court_df
    
    def __get_half_court_coordinates(self):
        '''
        Returns coordinates for the half court line.
        '''
        width = self.court_width 
        half_length = self.court_length / 2
        half_court_bounds = [[0, half_length, 0], [width, half_length, 0]]

        half_df = pd.DataFrame(half_court_bounds, columns=['x','y','z'])
        half_df['line_group'] = 'half_court'
        half_df['color'] = 'court'

        return half_df
    
    def __get_endzone_coordinates(self):
        endzone_length = 10
        length = 120
        width = self.court_width 
        
        endzone_lines = []
        
        # Left endzone line
        for y in range(endzone_length, length - endzone_length + 1, 10):
            endzone_lines.append([0, y, 0])
            endzone_lines.append([width, y, 0])
        
        # Right endzone line
        for y in range(endzone_length, length - endzone_length + 1, 10):
            endzone_lines.append([0, length - y, 0])
            endzone_lines.append([width, length - y, 0])

        endzone_df = pd.DataFrame(endzone_lines, columns=['x','y','z'])
        endzone_df['line_group'] = 'court'
        endzone_df['color'] = 'court'

        return endzone_df
    
    # def __get_endzone_coordinates(self):
    #     endzone_length = 10
    #     length = 120
    #     width = self.court_width 
    #     endzone_lines = [
    #         # Left endzone line
    #         [0, 10, 0],
    #         [width, 10, 0],
    #         [0,20,0],
    #         [width,20,0],
    #         [0,30,0],
    #         [width,30,0],
    #         [0,40,0],
    #         [width,40,0],
    #         [0,50,0],
    #         [width,50,0],
    #         [0,60,0],
    #         [width,60,0],
    #         [0,70,0],
    #         [width,70,0],
    #         [0,80,0],
    #         [width,80,0],
    #         [0,90,0],
    #         [width,90,0],
    #         [0,100,0],
    #         [width,100,0],
    #         # Right endzone line
    #         [0, 110, 0],
    #         [width, 110, 0],

    #         [width, 10, 0],
    #         [0, 10, 0],
    #         [width,20,0],
    #         [0,20,0],
    #         [width,30,0],
    #         [0,30,0],
    #         [width,40,0],
    #         [0,40,0],
    #         [width,50,0],
    #         [0,50,0],
    #         [width,60,0],
    #         [0,60,0],
    #         [width,70,0],
    #         [0,70,0],
    #         [width,80,0],
    #         [0,80,0],
    #         [width,90,0],
    #         [0,90,0],
    #         [width,100,0],
    #         [0,100,0],
    #         [width, 110, 0],
    #         [0, 110, 0],

    #     ]
        # endzonedf  = pd.DataFrame(endzone_lines, columns=['x','y','z'])
        # endzonedf['line_group'] = 'court'
        # endzonedf['color'] = 'a'

        # return endzonedf

    

    
    
    

    


    def get_court_lines(self):
        '''
        Returns a concatenated DataFrame of all the court coordinates 
        '''

        court_df = self.__get_court_perimeter_coordinates()
        half_df = self.__get_half_court_coordinates()
        endzone_df = self.__get_endzone_coordinates()
       

        court_lines_df = pd.concat([court_df, half_df,endzone_df])

        return court_lines_df