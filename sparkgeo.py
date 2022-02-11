#Python exercise for Sparkgeo
#Eddie Boyle
#Feb 2022

#import modules
import geopandas as gpd

#import data
lines = gpd.GeoDataFrame.from_file('lines.gpkg')
points = gpd.GeoDataFrame.from_file('points.gpkg')

#reproject to OSGB BNG
lines_osgb = lines.to_crs(epsg=27700)
points_osgb = points.to_crs(epsg=27700)

#create 500m buffer around lines, change CRS to BNG, and convert to GeoDataFrame
lines_buffer = lines_osgb.buffer(500)
lines_buffer_osgb = lines_buffer.to_crs(epsg=27700)
lines_buffer_osgb_gdf = gpd.GeoDataFrame(geometry=gpd.GeoSeries(lines_buffer_osgb))

#intersect points with buffer polygon, using spatial join
result_points = gpd.sjoin(points_osgb, lines_buffer_osgb_gdf, how='inner', op='intersects')

#export to geopackage
result_points.to_file("result_points.gpkg", layer='result_points', driver="GPKG")