import svgpathtools
import numpy as np
import csv


svg_file = ".img/debug.svg"

ip_steps = 8
scalingFactor = 10

def bezier_interpolate(p0, p1, p2, p3, t):
    return (1 - t)**3 * p0 + 3 * (1 - t)**2 * t * p1 + 3 * (1 - t) * t**2 * p2 + t**3 * p3

def convert(path, scale=scalingFactor, steps=ip_steps):
    paths, attributes = svgpathtools.svg2paths(path)
    lines = []

    # Process each path and convert to draw commands
    for path in paths:
        for segment in path:
            if isinstance(segment, svgpathtools.Line):
                start = segment.start
                end = segment.end
                lines.append((start, end))
            elif isinstance(segment, (svgpathtools.CubicBezier, svgpathtools.QuadraticBezier)):
                t_values = np.linspace(0, 1, steps)
                if isinstance(segment, svgpathtools.CubicBezier):
                    points = [bezier_interpolate(segment.start, segment.control1, segment.control2, segment.end, t) for t in t_values]
                elif isinstance(segment, svgpathtools.QuadraticBezier):
                    points = [bezier_interpolate(segment.start, segment.control, segment.control, segment.end, t) for t in t_values]
                for i in range(len(points) - 1):
                    lines.append((points[i], points[i + 1]))

    # Write the lines to a CSV file
    with open('path.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for line in lines:
            row = [line[0].real, line[0].imag, line[1].real, line[1].imag]
            writer.writerow([int(c * scale) for c in row])

def main():
    convert(svg_file, scalingFactor, ip_steps)

if __name__ == "__main__":
    main()
    print('Done!')

