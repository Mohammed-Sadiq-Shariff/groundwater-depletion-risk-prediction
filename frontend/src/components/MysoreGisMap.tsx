import React, { useState, useMemo, useRef } from "react";
import {
  ZoomIn,
  ZoomOut,
  RotateCcw,
  Layers,
  MapPin,
  Download,
  Info,
  Maximize2,
  Sparkles,
  ShieldAlert,
  Droplets,
  Eye,
  EyeOff,
} from "lucide-react";
import { MYSORE_GEOJSON, TalukFeature } from "../data/mysoreGeo";
import { StationTelemetry, Risk, TalukSummary } from "../types/dashboard";

interface MysoreGisMapProps {
  stations: StationTelemetry[]; // All 97 stations (or full set)
  matchingStationNames?: Set<string>; // Set of names that match active filters/search
  selectedStation: StationTelemetry | null;
  onSelectStation: (station: StationTelemetry) => void;
  selectedBlock: string;
  onSelectBlock: (block: string) => void;
  scenarioRainfall?: number;
  compact?: boolean;
}

// Bounding Box of Mysuru District
const BBOX = {
  minLon: 75.90868,
  maxLon: 77.13428,
  minLat: 11.73801,
  maxLat: 12.65568,
};

// Colors tuned for pristine WHITE map background
const RISK_COLORS: Record<Risk, { bg: string; fill: string; border: string; glow: string; text: string }> = {
  High: {
    bg: "rgba(254, 226, 226, 0.75)", // Soft light red
    fill: "#dc2626", // Crisp red marker
    border: "#ef4444",
    glow: "rgba(220, 38, 38, 0.55)",
    text: "#991b1b",
  },
  Moderate: {
    bg: "rgba(254, 243, 199, 0.70)", // Soft light amber
    fill: "#ea580c", // Crisp orange/amber
    border: "#f59e0b",
    glow: "rgba(234, 88, 12, 0.45)",
    text: "#92400e",
  },
  Low: {
    bg: "rgba(254, 249, 195, 0.65)", // Soft light yellow
    fill: "#ca8a04", // Crisp yellow/gold
    border: "#eab308",
    glow: "rgba(202, 138, 4, 0.40)",
    text: "#854d0e",
  },
  "No Depletion": {
    bg: "rgba(220, 252, 231, 0.70)", // Soft light green
    fill: "#16a34a", // Crisp emerald
    border: "#10b981",
    glow: "rgba(22, 163, 74, 0.45)",
    text: "#166534",
  },
};

export const MysoreGisMap: React.FC<MysoreGisMapProps> = ({
  stations,
  matchingStationNames,
  selectedStation,
  onSelectStation,
  selectedBlock,
  onSelectBlock,
  scenarioRainfall = 0,
  compact = false,
}) => {
  const svgRef = useRef<SVGSVGElement | null>(null);
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });

  const [hoveredTaluk, setHoveredTaluk] = useState<string | null>(null);
  const [hoveredStation, setHoveredStation] = useState<StationTelemetry | null>(null);
  const [tooltipPos, setTooltipPos] = useState({ x: 0, y: 0 });

  // Layer toggles
  const [showChoropleth, setShowChoropleth] = useState(true);
  const [showStations, setShowStations] = useState(true);
  const [showLabels, setShowLabels] = useState(true);
  const [showNonMatching, setShowNonMatching] = useState(true); // show all 97, dim non-matching

  const WIDTH = 920;
  const HEIGHT = 720;
  const PADDING = 45;

  // Projection math: Equirectangular onto SVG coordinates
  const project = useMemo(() => {
    const lonSpan = BBOX.maxLon - BBOX.minLon;
    const latSpan = BBOX.maxLat - BBOX.minLat;

    const scaleX = (WIDTH - 2 * PADDING) / lonSpan;
    const scaleY = (HEIGHT - 2 * PADDING) / latSpan;
    const scale = Math.min(scaleX, scaleY);

    const offX = PADDING + (WIDTH - 2 * PADDING - lonSpan * scale) / 2;
    const offY = PADDING + (HEIGHT - 2 * PADDING - latSpan * scale) / 2;

    return (lon: number, lat: number): [number, number] => {
      const x = offX + (lon - BBOX.minLon) * scale;
      const y = offY + (BBOX.maxLat - lat) * scale;
      return [x, y];
    };
  }, []);

  // Compute taluk aggregates and dominant risk
  const talukSummaries = useMemo<Record<string, TalukSummary>>(() => {
    const map: Record<string, TalukSummary> = {};

    MYSORE_GEOJSON.taluks.features.forEach((feat) => {
      const blockId = feat.properties.block;
      const blockName = feat.properties.name;
      const matchedStations = stations.filter(
        (s) =>
          s.block.toUpperCase() === blockId.toUpperCase() ||
          s.tehsil.toUpperCase() === blockId.toUpperCase()
      );

      const highCount = matchedStations.filter((s) => s.risk === "High").length;
      const modCount = matchedStations.filter((s) => s.risk === "Moderate").length;
      const lowCount = matchedStations.filter((s) => s.risk === "Low").length;
      const safeCount = matchedStations.filter((s) => s.risk === "No Depletion").length;

      let dominant: Risk = "No Depletion";
      if (highCount > 0 && highCount / (matchedStations.length || 1) >= 0.25) {
        dominant = "High";
      } else if (modCount >= lowCount && modCount >= safeCount && modCount > 0) {
        dominant = "Moderate";
      } else if (lowCount >= safeCount && lowCount > 0) {
        dominant = "Low";
      } else {
        dominant = "No Depletion";
      }

      const avgCur = matchedStations.length
        ? matchedStations.reduce((acc, s) => acc + s.current, 0) / matchedStations.length
        : 7.2;

      const avgPred = matchedStations.length
        ? matchedStations.reduce((acc, s) => acc + s.predicted, 0) / matchedStations.length
        : 7.4;

      map[blockId] = {
        block: blockId,
        taluk_name: blockName,
        station_count: matchedStations.length,
        avg_current_depth_m: Number(avgCur.toFixed(2)),
        avg_predicted_depth_m: Number(avgPred.toFixed(2)),
        dominant_risk: dominant,
        classification_color: RISK_COLORS[dominant].fill,
        risk_counts: {
          high: highCount,
          moderate: modCount,
          low: lowCount,
          no_depletion: safeCount,
        },
        center: feat.properties.center,
      };
    });

    return map;
  }, [stations]);

  // Convert GeoJSON polygon to SVG Path
  function coordinatesToSvgPath(geometry: any): string {
    if (!geometry || !geometry.coordinates) return "";

    const ringsToPath = (rings: number[][][]) => {
      return rings
        .map((ring) => {
          return (
            ring
              .map((coord, idx) => {
                const [px, py] = project(coord[0], coord[1]);
                return `${idx === 0 ? "M" : "L"} ${px.toFixed(1)} ${py.toFixed(1)}`;
              })
              .join(" ") + " Z"
          );
        })
        .join(" ");
    };

    if (geometry.type === "Polygon") {
      return ringsToPath(geometry.coordinates);
    } else if (geometry.type === "MultiPolygon") {
      return geometry.coordinates.map((polyRings: any) => ringsToPath(polyRings)).join(" ");
    }
    return "";
  }

  // District outer boundary path
  const districtPath = useMemo(() => {
    if (MYSORE_GEOJSON.district && MYSORE_GEOJSON.district.features?.length > 0) {
      return coordinatesToSvgPath(MYSORE_GEOJSON.district.features[0].geometry);
    }
    return "";
  }, [project]);

  // Mouse pan handling
  const handleMouseDown = (e: React.MouseEvent) => {
    if (e.button !== 0) return;
    setIsDragging(true);
    setDragStart({ x: e.clientX - pan.x, y: e.clientY - pan.y });
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    const rect = e.currentTarget.getBoundingClientRect();
    setTooltipPos({ x: e.clientX - rect.left, y: e.clientY - rect.top });

    if (isDragging) {
      setPan({
        x: e.clientX - dragStart.x,
        y: e.clientY - dragStart.y,
      });
    }
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  // Export SVG Snapshot
  const handleExportMap = () => {
    if (!svgRef.current) return;
    const svgData = new XMLSerializer().serializeToString(svgRef.current);
    const svgBlob = new Blob([svgData], { type: "image/svg+xml;charset=utf-8" });
    const svgUrl = URL.createObjectURL(svgBlob);
    const downloadLink = document.createElement("a");
    downloadLink.href = svgUrl;
    downloadLink.download = `mysore_groundwater_gis_map_${new Date().toISOString().slice(0, 10)}.svg`;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
    URL.revokeObjectURL(svgUrl);
  };

  const matchingCount = matchingStationNames
    ? stations.filter((s) => matchingStationNames.has(s.name)).length
    : stations.length;

  return (
    <div className={`gis-map-container white-theme ${compact ? "compact" : ""}`}>
      {/* MAP TOP TOOLBAR */}
      <div className="map-toolbar white-toolbar">
        <div className="map-title-badge">
          <div className="status-beacon live-green" />
          <div>
            <b className="text-navy">GENUINE MYSURU DISTRICT GIS MAP</b>
            <small className="text-subtle">
              Verified OpenStreetMap Taluk Boundaries & 97 CGWB Piezometer Stations
            </small>
          </div>
        </div>

        <div className="map-controls">
          <button
            type="button"
            className="ctrl-btn-white"
            title="Zoom In"
            onClick={() => setZoom((z) => Math.min(z + 0.3, 3.5))}
          >
            <ZoomIn size={16} />
          </button>
          <button
            type="button"
            className="ctrl-btn-white"
            title="Zoom Out"
            onClick={() => setZoom((z) => Math.max(z - 0.3, 0.7))}
          >
            <ZoomOut size={16} />
          </button>
          <button
            type="button"
            className="ctrl-btn-white"
            title="Reset View"
            onClick={() => {
              setZoom(1);
              setPan({ x: 0, y: 0 });
            }}
          >
            <RotateCcw size={16} />
          </button>

          <div className="divider-v-light" />

          {/* CHOROPLETH TOGGLE */}
          <button
            type="button"
            className={`ctrl-pill-white ${showChoropleth ? "active" : ""}`}
            onClick={() => setShowChoropleth(!showChoropleth)}
            title="Toggle Taluk Risk Coloring"
          >
            <Layers size={14} />
            <span>Risk Shading</span>
          </button>

          {/* STATIONS TOGGLE */}
          <button
            type="button"
            className={`ctrl-pill-white ${showStations ? "active" : ""}`}
            onClick={() => setShowStations(!showStations)}
            title="Toggle Station Markers"
          >
            <MapPin size={14} />
            <span>All Wells ({stations.length})</span>
          </button>

          {/* MATCHING TOGGLE */}
          {matchingStationNames && (
            <button
              type="button"
              className={`ctrl-pill-white ${showNonMatching ? "active" : ""}`}
              onClick={() => setShowNonMatching(!showNonMatching)}
              title={showNonMatching ? "Showing all with non-matching dimmed" : "Showing only matching"}
            >
              {showNonMatching ? <Eye size={14} /> : <EyeOff size={14} />}
              <span>Matching ({matchingCount})</span>
            </button>
          )}

          {/* EXPORT MAP SVG */}
          <button
            type="button"
            className="ctrl-btn-export"
            onClick={handleExportMap}
            title="Export Vector Map (SVG)"
          >
            <Download size={15} />
            <span>Export SVG</span>
          </button>
        </div>
      </div>

      {/* MAP CANVAS (WHITE BACKGROUND) */}
      <div
        className="svg-viewport white-canvas-viewport"
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        style={{ cursor: isDragging ? "grabbing" : "grab" }}
      >
        <svg
          ref={svgRef}
          viewBox={`0 0 ${WIDTH} ${HEIGHT}`}
          className="mysore-svg"
          style={{
            transform: `scale(${zoom}) translate(${pan.x}px, ${pan.y}px)`,
            transformOrigin: "center center",
            backgroundColor: "#ffffff",
          }}
        >
          <defs>
            {/* Filter for white background marker shadows */}
            <filter id="white-marker-shadow" x="-50%" y="-50%" width="200%" height="200%">
              <feDropShadow dx="0" dy="2" stdDeviation="2.5" floodColor="#0f172a" floodOpacity="0.28" />
            </filter>
            <filter id="taluk-hover-shadow" x="-10%" y="-10%" width="120%" height="120%">
              <feDropShadow dx="0" dy="3" stdDeviation="6" floodColor="#0284c7" floodOpacity="0.22" />
            </filter>

            {/* Subtle Cartographic Grid Pattern */}
            <pattern id="white-carto-grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path
                d="M 40 0 L 0 0 0 40"
                fill="none"
                stroke="#f1f5f9"
                strokeWidth="0.8"
              />
            </pattern>
          </defs>

          {/* BASE BACKGROUND: CRISP WHITE */}
          <rect width={WIDTH} height={HEIGHT} fill="#ffffff" />
          <rect width={WIDTH} height={HEIGHT} fill="url(#white-carto-grid)" opacity="0.8" />

          {/* DISTRICT OUTER PERIMETER */}
          {districtPath && (
            <path
              d={districtPath}
              className="district-perimeter-white"
              fill="none"
              stroke="#0284c7"
              strokeWidth="2.5"
              strokeDasharray="7 5"
              opacity="0.5"
            />
          )}

          {/* TALUK BOUNDARY POLYGONS */}
          <g className="taluks-layer">
            {MYSORE_GEOJSON.taluks.features.map((feat) => {
              const blockId = feat.properties.block;
              const pathData = coordinatesToSvgPath(feat.geometry);
              const summary = talukSummaries[blockId];
              const risk = summary?.dominant_risk || "No Depletion";
              const isSelected = selectedBlock.toUpperCase() === blockId.toUpperCase();
              const isHovered = hoveredTaluk === blockId;

              // Cartographic colors on white canvas
              const fillColor = showChoropleth
                ? isSelected
                  ? "rgba(2, 132, 199, 0.22)"
                  : isHovered
                  ? "rgba(224, 242, 254, 0.85)"
                  : RISK_COLORS[risk]?.bg || "#f8fafc"
                : isSelected
                ? "rgba(2, 132, 199, 0.15)"
                : isHovered
                ? "#e0f2fe"
                : "#f8fafc";

              const strokeColor = isSelected
                ? "#0284c7"
                : isHovered
                ? "#0284c7"
                : showChoropleth
                ? RISK_COLORS[risk]?.border || "#cbd5e1"
                : "#94a3b8";

              return (
                <path
                  key={blockId}
                  d={pathData}
                  className={`taluk-polygon-white ${isSelected ? "selected" : ""} ${isHovered ? "hovered" : ""}`}
                  fill={fillColor}
                  stroke={strokeColor}
                  strokeWidth={isSelected ? 3.2 : isHovered ? 2.5 : 1.4}
                  filter={isHovered ? "url(#taluk-hover-shadow)" : undefined}
                  onMouseEnter={() => setHoveredTaluk(blockId)}
                  onMouseLeave={() => setHoveredTaluk(null)}
                  onClick={() => onSelectBlock(selectedBlock === blockId ? "All Blocks" : blockId)}
                  style={{ cursor: "pointer", transition: "all 0.2s ease" }}
                />
              );
            })}
          </g>

          {/* TALUK CENTROID LABELS & WELL COUNTS */}
          {showLabels && (
            <g className="taluk-labels-layer" pointerEvents="none">
              {MYSORE_GEOJSON.taluks.features.map((feat) => {
                const blockId = feat.properties.block;
                const summary = talukSummaries[blockId];
                const center = feat.properties.center;
                if (!center) return null;
                const [cx, cy] = project(center[1], center[0]);
                const count = summary?.station_count || 0;
                const isSelected = selectedBlock.toUpperCase() === blockId.toUpperCase();

                return (
                  <g key={`lbl-${blockId}`} transform={`translate(${cx}, ${cy})`}>
                    <rect
                      x="-60"
                      y="-14"
                      width="120"
                      height="28"
                      rx="8"
                      fill="#ffffff"
                      stroke={isSelected ? "#0284c7" : "#cbd5e1"}
                      strokeWidth={isSelected ? 2 : 1}
                      filter="url(#white-marker-shadow)"
                    />
                    <text
                      x="0"
                      y="1"
                      textAnchor="middle"
                      fill={isSelected ? "#0369a1" : "#0f172a"}
                      fontSize="10.5"
                      fontWeight="700"
                      fontFamily="inherit"
                    >
                      {feat.properties.name}
                    </text>
                    <text
                      x="0"
                      y="11"
                      textAnchor="middle"
                      fill="#64748b"
                      fontSize="8.5"
                      fontWeight="600"
                      fontFamily="inherit"
                    >
                      {count} wells
                    </text>
                  </g>
                );
              })}
            </g>
          )}

          {/* ALL 97 MONITORING STATIONS WITH EXACT GPS COORDINATES */}
          {showStations && (
            <g className="stations-layer">
              {stations.map((st) => {
                const [sx, sy] = project(st.longitude, st.latitude);
                const isSelected = selectedStation?.name === st.name;
                const isHighRisk = st.risk === "High";
                const riskStyle = RISK_COLORS[st.risk] || RISK_COLORS["Low"];

                // Check match with active multi-filters/search
                const isMatching = matchingStationNames ? matchingStationNames.has(st.name) : true;

                // If non-matching are hidden completely
                if (!isMatching && !showNonMatching) return null;

                const opacity = isMatching ? 1 : 0.22;
                const radius = isSelected ? 8 : isMatching ? 5.5 : 4;

                return (
                  <g
                    key={st.name}
                    transform={`translate(${sx}, ${sy})`}
                    className={`station-marker-white ${isSelected ? "selected" : ""} ${!isMatching ? "dimmed" : ""}`}
                    opacity={opacity}
                    onClick={(e) => {
                      e.stopPropagation();
                      onSelectStation(st);
                    }}
                    onMouseEnter={() => setHoveredStation(st)}
                    onMouseLeave={() => setHoveredStation(null)}
                    style={{ cursor: "pointer" }}
                  >
                    {/* Animated Pulsing Halo for High-Risk Stations */}
                    {isHighRisk && isMatching && (
                      <circle
                        r="14"
                        fill="none"
                        stroke="#dc2626"
                        strokeWidth="1.6"
                        className="pulse-halo-white"
                        opacity="0.75"
                      />
                    )}

                    {/* Selected Targeting Crosshair */}
                    {isSelected && (
                      <g className="target-crosshair-white">
                        <circle
                          r="18"
                          fill="none"
                          stroke="#0284c7"
                          strokeWidth="2.2"
                          strokeDasharray="4 3"
                          className="spin-crosshair"
                        />
                        <line x1="-22" y1="0" x2="-14" y2="0" stroke="#0284c7" strokeWidth="2" />
                        <line x1="14" y1="0" x2="22" y2="0" stroke="#0284c7" strokeWidth="2" />
                        <line x1="0" y1="-22" x2="0" y2="-14" stroke="#0284c7" strokeWidth="2" />
                        <line x1="0" y1="14" x2="0" y2="22" stroke="#0284c7" strokeWidth="2" />
                      </g>
                    )}

                    {/* Outer Drop Shadow Halo */}
                    <circle
                      r={radius}
                      fill={riskStyle.fill}
                      stroke="#ffffff"
                      strokeWidth={isSelected ? 3 : 2}
                      filter="url(#white-marker-shadow)"
                    />

                    {/* Inner Pin Point for Precision Acuity */}
                    <circle r={radius * 0.4} fill="#ffffff" />
                  </g>
                );
              })}
            </g>
          )}
        </svg>

        {/* MAP LEGEND ON WHITE CANVAS */}
        <div className="map-legend-white">
          <div className="legend-header">
            <ShieldAlert size={13} className="text-navy" />
            <span>WELL DEPLETION RISK</span>
          </div>
          <div className="legend-items-row">
            <div className="legend-item">
              <span className="dot red" />
              <span>High Risk</span>
            </div>
            <div className="legend-item">
              <span className="dot orange" />
              <span>Moderate</span>
            </div>
            <div className="legend-item">
              <span className="dot yellow" />
              <span>Low Risk</span>
            </div>
            <div className="legend-item">
              <span className="dot green" />
              <span>No Depletion</span>
            </div>
          </div>
        </div>

        {/* HOVER TOOLTIP ON WHITE MAP */}
        {hoveredStation && (
          <div
            className="map-tooltip-card-white"
            style={{
              left: Math.min(tooltipPos.x + 14, WIDTH - 270),
              top: Math.max(tooltipPos.y - 120, 20),
            }}
          >
            <div className="tooltip-header">
              <div>
                <b className="station-name">{hoveredStation.name}</b>
                <small className="station-sub">
                  {hoveredStation.village} • {hoveredStation.block}
                </small>
              </div>
              <span
                className="risk-tag"
                style={{
                  background: RISK_COLORS[hoveredStation.risk].bg,
                  color: RISK_COLORS[hoveredStation.risk].text,
                  border: `1px solid ${RISK_COLORS[hoveredStation.risk].border}`,
                }}
              >
                {hoveredStation.risk}
              </span>
            </div>

            <div className="tooltip-metrics-grid">
              <div className="t-metric">
                <small>Current Depth</small>
                <b>{hoveredStation.current.toFixed(2)}m</b>
              </div>
              <div className="t-metric">
                <small>Forecast Depth</small>
                <b>{hoveredStation.predicted.toFixed(2)}m</b>
              </div>
              <div className="t-metric">
                <small>Projected Change</small>
                <b
                  style={{
                    color: hoveredStation.change > 0 ? "#dc2626" : "#16a34a",
                  }}
                >
                  {hoveredStation.change > 0 ? "+" : ""}
                  {hoveredStation.change.toFixed(2)}m
                </b>
              </div>
              <div className="t-metric">
                <small>GPS Coordinates</small>
                <span>
                  {hoveredStation.latitude.toFixed(3)}°N, {hoveredStation.longitude.toFixed(3)}°E
                </span>
              </div>
            </div>

            <div className="tooltip-click-hint">Click well to view full telemetry & charts</div>
          </div>
        )}
      </div>

      {/* MAP BOTTOM STATS STRIP */}
      <div className="map-bottom-strip white-strip">
        <div className="strip-col">
          <small>ALL CGWB STATIONS</small>
          <b>{stations.length}</b>
        </div>
        <div className="divider-v-light" />
        <div className="strip-col">
          <small>FILTERED MATCHES</small>
          <b className="text-cyan-bold">{matchingCount}</b>
        </div>
        <div className="divider-v-light" />
        <div className="strip-col">
          <small>HIGH RISK WELLS</small>
          <b className="text-red">
            {stations.filter((s) => s.risk === "High").length}
          </b>
        </div>
        <div className="divider-v-light" />
        <div className="strip-col">
          <small>AVERAGE WATER TABLE</small>
          <b>
            {(stations.reduce((a, b) => a + b.current, 0) / (stations.length || 1)).toFixed(2)}m
          </b>
        </div>
        <div className="divider-v-light" />
        <div className="strip-col">
          <small>SELECTED TALUK</small>
          <b className="text-navy">{selectedBlock}</b>
        </div>
      </div>
    </div>
  );
};
