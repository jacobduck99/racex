import { useMemo } from "react";

interface Coordinates {
  lon: number;
  lat: number;
  sector_start_lon?: number;
  sector_start_lat?: number;
  sector_end_lon?: number;
  sector_end_lat?: number;
}

interface SectorAnalysis {
  sector: number;
  delta: number;
  braking?: string;
  gear?: string;
  throttle?: string;
}

interface BuildTrackMapProps {
  coordinates: Coordinates[];
  sectorAnalysis?: SectorAnalysis[];
  width?: number;
  height?: number;
}

const NEUTRAL_THRESHOLD = 0.05;

function cornerColor(delta: number | undefined): string {
  if (delta === undefined) return "#facc15";
  if (Math.abs(delta) < NEUTRAL_THRESHOLD) return "#94a3b8";
  if (delta < 0) return "#22c55e";
  return "#ef4444";
}

function minDistSqToTrack(px: number, py: number, track: { x: number; y: number }[]): number {
  let best = Infinity;
  for (const p of track) {
    const dx = p.x - px;
    const dy = p.y - py;
    const d = dx * dx + dy * dy;
    if (d < best) best = d;
  }
  return best;
}

export default function BuildTrackMap({
  coordinates,
  sectorAnalysis,
  width = 800,
  height = 600,
}: BuildTrackMapProps) {
  const { points, sectorMarkers, deltaBySector } = useMemo(() => {
    const deltaBySector = new Map<number, number>();
    if (sectorAnalysis) {
      for (const s of sectorAnalysis) {
        deltaBySector.set(s.sector, s.delta);
      }
    }

    if (!coordinates || coordinates.length === 0) {
      return { points: "", sectorMarkers: [], deltaBySector };
    }

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
    const marginFactor = 0.80;
    const scale = marginFactor * Math.min(width / lonRange, height / latRange);

    const toXY = (lon: number, lat: number) => ({
      x: (lon - centerLon) * scale + width / 2,
      y: (centerLat - lat) * scale + height / 2,
    });

    const xyCoords = coordinates.map((c) => toXY(c.lon, c.lat));
    const points = xyCoords.map(({ x, y }) => `${x},${y}`).join(" ");

    const LABEL_PROBE = 32;

    const sectorMarkers: {
      x: number;
      y: number;
      px: number;
      py: number;
      sideSign: 1 | -1;
      type: "start" | "end";
      index: number;
    }[] = [];
    let sectorIndex = 0;

    const pushMarker = (
      x: number,
      y: number,
      i: number,
      type: "start" | "end",
      index: number
    ) => {
      const prev = xyCoords[Math.max(0, i - 3)];
      const next = xyCoords[Math.min(xyCoords.length - 1, i + 3)];
      const dx = next.x - prev.x;
      const dy = next.y - prev.y;
      const len = Math.sqrt(dx * dx + dy * dy) || 1;
      const px = -dy / len;
      const py = dx / len;

      const posA = { x: x + px * LABEL_PROBE, y: y + py * LABEL_PROBE };
      const posB = { x: x - px * LABEL_PROBE, y: y - py * LABEL_PROBE };
      const dA = minDistSqToTrack(posA.x, posA.y, xyCoords);
      const dB = minDistSqToTrack(posB.x, posB.y, xyCoords);
      const sideSign: 1 | -1 = dA >= dB ? 1 : -1;

      sectorMarkers.push({ x, y, px, py, sideSign, type, index });
    };

    coordinates.forEach((c, i) => {
      if (c.sector_start_lon != null && c.sector_start_lat != null) {
        const { x, y } = toXY(c.sector_start_lon, c.sector_start_lat);
        pushMarker(x, y, i, "start", sectorIndex++);
      }
      if (c.sector_end_lon != null && c.sector_end_lat != null) {
        const { x, y } = toXY(c.sector_end_lon, c.sector_end_lat);
        pushMarker(x, y, i, "end", sectorIndex);
      }
    });

    return { points, sectorMarkers, deltaBySector };
  }, [coordinates, width, height, sectorAnalysis]);

  if (!coordinates || coordinates.length === 0) {
    return <p className="text-slate-400">No track data</p>;
  }

  const LINE_HALF = 9;
  const LABEL_OFFSET = 32;

  return (
    <svg width={width} height={height} style={{ background: "transparent" }}>
      <polyline points={points} fill="none" stroke="#000" strokeWidth={36} strokeLinejoin="round" strokeLinecap="round" opacity={0.6} />
      <polyline points={points} fill="none" stroke="#00ff88" strokeWidth={30} strokeLinejoin="round" strokeLinecap="round" />
      <polyline points={points} fill="none" stroke="#0f172a" strokeWidth={22} strokeLinejoin="round" strokeLinecap="round" />
      <polyline points={points} fill="none" stroke="#1e293b" strokeWidth={2} strokeLinejoin="round" strokeLinecap="round" strokeDasharray="8 12" />

      {sectorMarkers.map((m, i) => {
        const isStart = m.type === "start";
        const tickColor = isStart ? "#facc15" : "#f43f5e";
        const x1 = m.x - m.px * LINE_HALF;
        const y1 = m.y - m.py * LINE_HALF;
        const x2 = m.x + m.px * LINE_HALF;
        const y2 = m.y + m.py * LINE_HALF;
        const labelX = m.x + m.px * m.sideSign * LABEL_OFFSET;
        const labelY = m.y + m.py * m.sideSign * LABEL_OFFSET;

        const sectorNumber = m.index + 1;
        const delta = isStart ? deltaBySector.get(sectorNumber) : undefined;
        const circleColor = isStart ? cornerColor(delta) : tickColor;

        return (
          <g key={i}>
            <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={tickColor} strokeWidth={6} strokeLinecap="round" opacity={0.3} />
            <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={tickColor} strokeWidth={2.5} strokeLinecap="round" />
            {isStart && (
              <>
                <circle cx={labelX} cy={labelY} r={12} fill={circleColor} opacity={0.18} />
                <circle cx={labelX} cy={labelY} r={11} fill="none" stroke={circleColor} strokeWidth={1.5} opacity={0.85} />
                <text
                  x={labelX}
                  y={labelY + 4}
                  fill={circleColor}
                  fontSize={11}
                  fontFamily="ui-monospace, monospace"
                  fontWeight="800"
                  textAnchor="middle"
                >
                  C{sectorNumber}
                </text>
              </>
            )}
          </g>
        );
      })}
    </svg>
  );
}
