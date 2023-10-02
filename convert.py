import argparse
import sys
import csv
import gpxpy
import gpxpy.gpx

def main(argv):
    parser = argparse.ArgumentParser(description='Convert Steps data to GMX')
    parser.add_argument('--input', help='input steps data file.')
    parser.add_argument('--output', help='output gmx data file.')

    args = parser.parse_args(argv)
    input = args.input
    if not input:
        raise 'must support input file name.'
    output = args.output if args.output else 'output.gpx'

    print(f'Read input file {input} and write to file {output}')

    gpx = gpxpy.gpx.GPX()

    with open(input, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            [gui, loc_type, lo, la, heading, accuracy, speed, distance, is_back, step_type, altitude] = row
            print(f'append {lo} {la}')
            # Create first track in our GPX:
            gpx_track = gpxpy.gpx.GPXTrack()
            gpx.tracks.append(gpx_track)
            # Create first segment in our GPX track:
            gpx_segment = gpxpy.gpx.GPXTrackSegment()
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(la, lo, elevation=heading, speed=speed))
            gpx_track.segments.append(gpx_segment)
        print(f'write {len(row)} lines to gpx')
    with open(output, 'w') as gpxfile:
        out = gpx.to_xml()
        print(f'{out}')
        gpxfile.write(out)

if __name__ == "__main__":
    main(sys.argv[1:])
