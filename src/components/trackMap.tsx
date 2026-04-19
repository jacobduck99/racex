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
    const marginFactor = 0.90;
    const scale = marginFactor * Math.min(width / lonRange, height / latRange);

    const toXY = (lon: number, lat: number) => ({
      x: (lon - centerLon) * scale + width / 2,
      y: (centerLat - lat) * scale + height / 2,
    });

    const xyCoords = coordinates.map((c) => toXY(c.lon, c.lat));
    const points = xyCoords.map(({ x, y }) => `${x},${y}`).join(" ");

    const sectorMarkers: { x: number; y: number; px: number; py: number; type: "start" | "end"; index: number }[] = [];
    let sectorIndex = 0;

    coordinates.forEach((c, i) => {
      if (c.sector_start_lon != null && c.sector_start_lat != null) {
        const { x, y } = toXY(c.sector_start_lon, c.sector_start_lat);
        const prev = xyCoords[Math.max(0, i - 3)];
        const next = xyCoords[Math.min(xyCoords.length - 1, i + 3)];
        const dx = next.x - prev.x;
        const dy = next.y - prev.y;
        const len = Math.sqrt(dx * dx + dy * dy) || 1;
        sectorMarkers.push({ x, y, px: -dy / len, py: dx / len, type: "start", index: sectorIndex++ });
      }
      if (c.sector_end_lon != null && c.sector_end_lat != null) {
        const { x, y } = toXY(c.sector_end_lon, c.sector_end_lat);
        const prev = xyCoords[Math.max(0, i - 3)];
        const next = xyCoords[Math.min(xyCoords.length - 1, i + 3)];
        const dx = next.x - prev.x;
        const dy = next.y - prev.y;
        const len = Math.sqrt(dx * dx + dy * dy) || 1;
        sectorMarkers.push({ x, y, px: -dy / len, py: dx / len, type: "end", index: sectorIndex });
      }
    });

    return { points, sectorMarkers };
  }, [coordinates, width, height]);

  if (!coordinates || coordinates.length === 0) {
    return <p className="text-slate-400">No track data</p>;
  }

  const LINE_HALF = 10;

  return (
    <svg width={width} height={height} style={{ background: "transparent" }}>
      <defs>
        <filter id="subtle-glow">
          <feGaussianBlur stdDeviation="2" result="coloredBlur" />
          <feMerge>
            <feMergeNode in="coloredBlur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>

      {/* Shadow */}
      <polyline points={points} fill="none" stroke="#000" strokeWidth={36} strokeLinejoin="round" strokeLinecap="round" opacity={0.6} />
      {/* Colored border */}
      <polyline points={points} fill="none" stroke="#00ff88" strokeWidth={30} strokeLinejoin="round" strokeLinecap="round" />
      {/* Dark road */}
      <polyline points={points} fill="none" stroke="#0f172a" strokeWidth={22} strokeLinejoin="round" strokeLinecap="round" />
      {/* Center line */}
      <polyline points={points} fill="none" stroke="#1e293b" strokeWidth={2} strokeLinejoin="round" strokeLinecap="round" strokeDasharray="8 12" />

      {sectorMarkers.map((m, i) => {
        const isStart = m.type === "start";
        const color = isStart ? "#facc15" : "#f43f5e";
        const x1 = m.x - m.px * LINE_HALF;
        const y1 = m.y - m.py * LINE_HALF;
        const x2 = m.x + m.px * LINE_HALF;
        const y2 = m.y + m.py * LINE_HALF;
        const label = isStart ? `S${m.index + 1}` : "";
        const side = m.index % 2 === 0 ? 1 : -1;
        const labelX = m.x + m.px * side * 32;
        const labelY = m.y + m.py * side * 32;
        return (
          <g key={i}>
            {/* Outer glow */}
            <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={color} strokeWidth={6} strokeLinecap="round" opacity={0.3} />
            {/* Main line */}
            <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={color} strokeWidth={2.5} strokeLinecap="round" />
            {isStart && (
              <>
                <circle cx={labelX} cy={labelY} r={12} fill={color} opacity={0.15} />
                <circle cx={labelX} cy={labelY} r={11} fill="none" stroke={color} strokeWidth={1.5} opacity={0.8} />
                <text
                  x={labelX}
                  y={labelY + 4}
                  fill={color}
                  fontSize={11}
                  fontFamily="ui-monospace, monospace"
                  fontWeight="800"
                  textAnchor="middle"
                >
                  {label}
                </text>
              </>
            )}
          </g>
        );
      })}
    </svg>
  );
}
