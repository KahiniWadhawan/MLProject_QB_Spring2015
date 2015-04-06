# -*- coding: utf-8 -*-


class FeatureExtractor(object):
    def __init__(self, trip):
        self.trip = trip       
        
    def speed(self, **trip):
        None
    
        
    def stops(self):
        '''returns stop coordinates and indices in a given trip'''
        stop_coordinates = []
        stop_indices = []
        len_trip = len(self.trip)
        reverse_trip = [x for x in reversed(self.trip)]
        prev_stop = None
        
        for i in xrange(1, len_trip): 
            if reverse_trip[i - 1] == prev_stop:
                continue
            
            if reverse_trip[i - 1] == reverse_trip[i]:
                stop_coordinates.append(reverse_trip[i - 1])
                stop_indices.append(len_trip - i)
                prev_stop = reverse_trip[i]
                
        return stop_coordinates, stop_indices
        
    def num_stops(self):
        '''calculates number of trips in a given trip'''
        stop_coordinates, stop_indices = self.stops()
        return len(stop_indices)
                
    def speed_at_stops(self):
        '''calculates speed at stops for a list of trip'''
        stop_coordinates, stop_indices = self.stops()
        speed_at_stops_list = []
        
        for stop_index in stop_indices:
            speed_at_stops_list.append(self.speed(self.trip[stop_index: stop_index + 10]))
            
        return speed_at_stops_list
            




if __name__ == "__main__":
    # Test
    trip = [(1, 2), (1, 1), (1, 1), (2, 2), (2, 1), (2, 1), (3,2)]
    f = FeatureExtractor(trip)
    print f.stops()
    print f.num_stops()
    
    