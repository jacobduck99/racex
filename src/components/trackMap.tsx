import { useMemo } from "react";

interface Coordinates {
  lon: number;
  lat: number;
  sector_start_lon?: number;
  sector_start_lat?: number;
  sector_end_lon?: number;
  sector_end_lat?: number;
}

interface BuildTrackMapProps {
  coordinates: Coordinates[];
  width?: number;
  height?: number;
}

export default function BuildTrackMap({ coordinates, width = 800, height = 600 }: BuildTrackMapProps) {
  const { points, sectorMarkers } = useMemo(() => {
    if (!coordinates || coordinates.length === 0) return { points: "", sectorMarkers: [] };

    const lons = coordinates.map((c) => c.lon);
    const lats = coordinates.map((c) => c.lat);
    const minLon = Math.min(...lons);
    const maxLon = Math.max(...lons);
    const minLat = Math.min(...lats);
    const maxLat = Math.max(...lats);
    const lonRange = maxLon - minLon || 1;
    const latRange = maxLat - minLat || 1;
    const centerLon = (minLon + maxLon) / 2;
    const centerLat = (minLat + maxLat) / 2;
    const marginFactor = 0.98;
    const scale = marginFactor * Math.min(width / lonRange, height / latRange);

    const toXY = (lon: number, lat: number) => ({
      x: (lon - centerLon) * scale + width / 2,
      y: (centerLat - lat) * scale + height / 2,
    });

    const xyCoords = coordinates.map((c) => toXY(c.lon, c.lat));

    const points = xyCoords.map(({ x, y }) => `${x},${y}`).join(" ");

    const getPerp = (idx: number) => {
      const prev = xyCoords[Math.max(0, idx - 1)];
      const next = xyCoords[Math.min(xyCoords.length - 1, idx + 1)];
      const dx = next.x - prev.x;
      const dy = next.y - prev.y;
      const len = Math.sqrt(dx * dx + dy * dy) || 1;
      // perpendicular is (-dy, dx) normalised
      return { px: -dy / len, py: dx / len };
    };

    const sectorMarkers: { x: number; y: number; px: number; py: number; type: "start" | "end"; index: number }[] = [];
    let sectorIndex = 0;

    coordinates.forEach((c, i) => {
      if (c.sector_start_lon != null && c.sector_start_lat != null) {
        const { x, y } = toXY(c.sector_start_lon, c.sector_start_lat);
        const { px, py } = getPerp(i);
        sectorMarkers.push({ x, y, px, py, type: "start", index: sectorIndex++ });
      }
      if (c.sector_end_lon != null && c.sector_end_lat != null) {
        const { x, y } = toXY(c.sector_end_lon, c.sector_end_lat);
        const { px, py } = getPerp(i);
        sectorMarkers.push({ x, y, px, py, type: "end", index: sectorIndex });
      }
    });

    return { points, sectorMarkers };
  }, [coordinates, width, height]);

  if (!coordinates || coordinates.length === 0) {
    return <p>No track data</p>;
  }

  const LINE_HALF = 14;

  return (
    <svg width={width} height={height} style={{ background: "transparent" }}>
      <defs>
        <filter id="glow">
          <feGaussianBlur stdDeviation="3" result="coloredBlur" />
          <feMerge>
            <feMergeNode in="coloredBlur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>

      <polyline
        points={points}
        fill="none"
        stroke="#1a1a1a"
        strokeWidth={12}
        strokeLinejoin="round"
        strokeLinecap="round"
      />
      <polyline
        points={points}
        fill="none"
        stroke="#00ff88"
        strokeWidth={4}
        strokeLinejoin="round"
        strokeLinecap="round"
        filter="url(#glow)"
      />

      {sectorMarkers.map((m, i) => {
        const isStart = m.type === "start";
        const color = isStart ? "#ffffff" : "#ff4444";
        const label = isStart ? `S${m.index + 1}` : "";
        const x1 = m.x - m.px * LINE_HALF;
        const y1 = m.y - m.py * LINE_HALF;
        const x2 = m.x + m.px * LINE_HALF;
        const y2 = m.y + m.py * LINE_HALF;
        return (
          <g key={i}>
            <line
              x1={x1} y1={y1} x2={x2} y2={y2}
              stroke={color}
              strokeWidth={isStart ? 3 : 2}
              strokeLinecap="round"
              opacity={0.9}
              filter="url(#glow)"
            />
            <circle cx={m.x} cy={m.y} r={3} fill={color} opacity={0.95} />
            {label && (
              <text
                x={x2 + 5}
                y={y2 + 4}
                fill={color}
                fontSize={11}
                fontFamily="monospace"
                opacity={0.85}
              >
                {label}
              </text>
            )}
          </g>
        );
      })}
    </svg>
  );
}
