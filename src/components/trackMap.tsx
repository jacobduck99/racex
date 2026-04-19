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

    const padding = 40;
    const drawWidth = width - padding * 2;
    const drawHeight = height - padding * 2;

    const scale = Math.min(drawWidth / lonRange, drawHeight / latRange);

    return coordinates
      .map((c) => {
        const x = (c.lon - minLon) * scale + padding;
        const y = (maxLat - c.lat) * scale + padding;
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
        strokeWidth={2}
        strokeLinejoin="round"
        strokeLinecap="round"
      />
    </svg>
  );
}
