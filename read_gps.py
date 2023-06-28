import exifread
import sys
import os
from os import walk
import argparse
import gpxpy
import gpxpy.gpx

# barrowed from 
# https://gist.github.com/snakeye/fdc372dbf11370fe29eb 
def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)

def read_gps(file_name: str):
    if not os.path.exists(file_name):
        return (-1, -1)
    
    with open(file_name, 'rb') as f:
        exif_dict = exifread.process_file(f)
        print('DateTime: ', exif_dict.get('EXIF DateTimeOriginal'))
        print('CAMERA Make: ', exif_dict.get('Image Make'))
        print('CAMERA: ', exif_dict.get('Image Model'))
        print('SIZE: ', exif_dict.get('EXIF ExifImageWidth'), exif_dict.get('EXIF ExifImageLength'))
        latitude = exif_dict.get('GPS GPSLatitude')
        latitude_ref = exif_dict.get('GPS GPSLatitudeRef')
        longitude = exif_dict.get('GPS GPSLongitude')
        longitude_ref = exif_dict.get('GPS GPSLongitudeRef')
        if latitude:
            lat_value = _convert_to_degress(latitude)
            if latitude_ref.values != 'N':
                lat_value = -lat_value
        else:
            return (-1, -1)
        if longitude:
            lon_value = _convert_to_degress(longitude)
            if longitude_ref.values != 'E':
                lon_value = -lon_value
        else:
            return (-1, -1)
        return (lat_value, lon_value)

def main(argv):
    parser = argparse.ArgumentParser(description='Read gps pos in dir.')
    parser.add_argument('--input', help='input dir.')
    parser.add_argument('--output', help='output gmx data file.')

    args = parser.parse_args(argv)
    input = args.input
    if not input:
        raise 'must support input file name.'
    output = args.output if args.output else 'generated.gpx'

    print(f'Read input file {input} and write to file {output}')

    gpx = gpxpy.gpx.GPX()

    # Create first track in our GPX:
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    files = []
    for (dirpath, dirnames, filenames) in walk(input):
        for name in filenames:
            full_name = os.path.join(dirpath, name)
            files.append(full_name)

    for f in files:
        a, b = read_gps(f)
        if a == -1 and b == -1:
            continue;
        print(f'GPS: {a}, {b}')
            # Create first segment in our GPX track:
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(a, b))

    with open(output, 'w') as gpxfile:
        gpxfile.write(gpx.to_xml())

if __name__ == "__main__":
    main(sys.argv[1:])
