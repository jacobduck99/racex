import { useMemo } from "react";

interface Coordinates {
  lon: number;
  lat: number;
}

interface BuildTrackMapProps {
  coordinates: Coordinates[];
  width?: number;
  height?: number;
}

export default function BuildTrackMap({ coordinates, width = 800, height = 600 }: BuildTrackMapProps) {
  const points = useMemo(() => {
    if (!coordinates || coordinates.length === 0) return "";

    const lons = coordinates.map((c) => c.lon);
    const lats = coordinates.map((c) => c.lat);

    const minLon = Math.min(...lons);
    const maxLon = Math.max(...lons);
    const minLat = Math.min(...lats);
    const maxLat = Math.max(...lats);

    const lonRange = maxLon - minLon || 1;
    const latRange = maxLat - minLat || 1;

    // Center of the track in lon/lat space
    const centerLon = (minLon + maxLon) / 2;
    const centerLat = (minLat + maxLat) / 2;

    // Margin factor so it doesn't touch the edges (0.9 = 10% margin)
    const marginFactor = 0.98;

    // Compute scale to fit into SVG with margin
    const scale = marginFactor * Math.min(width / lonRange, height / latRange);

    return coordinates
      .map((c) => {
        // Shift so center of track maps to center of SVG
        const x = (c.lon - centerLon) * scale + width / 2;
        const y = (centerLat - c.lat) * scale + height / 2;
        return `${x},${y}`;
      })
      .join(" ");
  }, [coordinates, width, height]);

  if (!coordinates || coordinates.length === 0) {
    return <p>No track data</p>;
  }

  return (
    <svg width={width} height={height} style={{ background: "transparent" }}>
      <polyline
        points={points}
        fill="none"
        stroke="#00ff88"
        strokeWidth={8} // make this bigger if you want it even chunkier
        strokeLinejoin="round"
        strokeLinecap="round"
      />
    </svg>
  );
}

