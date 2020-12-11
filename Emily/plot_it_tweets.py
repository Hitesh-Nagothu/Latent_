import json
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from matplotlib.patches import Circle

# THIS IS NOT WORKING... running cartopy on windows causes major isses
# and I almost deleted System32 trying to get the packages to work.
# I believe with a few extra lines and tweaks, this code could work
# however I am unable to figure it out at this time :(
def plot_it_tweets():
    inFile = 'solr_it_geocoded.json'
    # Read from json file and output tp pandas df
    df = pd.read_json(inFile)
        
    # Sets up general setting for MatPlotLib
    plt.style.use('FiveThirtyEight')
    plt.rcParams.update({'font.size': 20})
    plt.rcParams['figure.figsize'] = (20, 10)
    
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.stock_img()
    # plot individual locations                                                                                                       
    ax.plot(mapdata.lon, mapdata.lat, 'ro', transform=ccrs.PlateCarree())
    # add coastlines for reference                                                                                                
    ax.coastlines(resolution='50m')
    ax.set_global()
    ax.set_extent([20, -20, 45,60])
    def get_radius(freq):
        if freq < 50:
            return 0.5
        elif freq < 200:
            return 1.2
        elif freq < 1000:
            return 1.8
    # plot count of tweets per location
    for i,x in locations.iteritems():
        ax.add_patch(Circle(xy=[i[2], i[1]], radius=get_radius(x), color='blue', alpha=0.6, transform=ccrs.PlateCarree()))
    plt.show()
    
if __name__ == "__main__":
    plot_it_tweets()