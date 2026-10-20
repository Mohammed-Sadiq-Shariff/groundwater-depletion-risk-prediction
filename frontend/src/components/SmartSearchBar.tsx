import React, { useState, useRef, useEffect, useMemo } from "react";
import { Search, MapPin, Map as MapIcon, ShieldAlert, X, ChevronRight, Sparkles } from "lucide-react";
import { StationTelemetry, Risk } from "../types/dashboard";

interface SmartSearchBarProps {
  stations: StationTelemetry[];
  onSelectStation: (station: StationTelemetry) => void;
  onSelectTaluk: (taluk: string) => void;
  onSelectRisk?: (risk: Risk) => void;
  searchQuery: string;
  onSearchChange: (query: string) => void;
  className?: string;
}

const TALUKS_INFO = [
  { id: "MYSORE", name: "Mysuru", alias: "Mysore" },
  { id: "HUNSUR", name: "Hunsur", alias: "Hunsur" },
  { id: "KRISHNARAJANAGARA", name: "Krishnarajanagara", alias: "KR Nagar" },
  { id: "NANJANGUD", name: "Nanjangud", alias: "Nanjangud" },
  { id: "PIRIYAPATNA", name: "Piriyapatna", alias: "Periyapatna" },
  { id: "TIRUMAKUDAL-NARSIPUR", name: "Tirumakudal Narsipur", alias: "TN Pura" },
  { id: "HEGGADADEVANKOTE", name: "Heggadadevankote", alias: "HD Kote" },
  { id: "SARAGUR", name: "Saragur", alias: "Saragur" },
  { id: "SALIGRAMA", name: "Saligrama", alias: "Saligrama" },
];

const RISK_BADGES: Record<Risk, { label: string; color: string; bg: string }> = {
  High: { label: "High Risk", color: "#ef4444", bg: "rgba(239, 68, 68, 0.15)" },
  Moderate: { label: "Moderate", color: "#f59e0b", bg: "rgba(245, 158, 11, 0.15)" },
  Low: { label: "Low Risk", color: "#eab308", bg: "rgba(234, 179, 8, 0.15)" },
  "No Depletion": { label: "Safe", color: "#10b981", bg: "rgba(16, 185, 129, 0.15)" },
};

export const SmartSearchBar: React.FC<SmartSearchBarProps> = ({
  stations,
  onSelectStation,
  onSelectTaluk,
  onSelectRisk,
  searchQuery,
  onSearchChange,
  className = "",
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const containerRef = useRef<HTMLDivElement | null>(null);
  const inputRef = useRef<HTMLInputElement | null>(null);

  // Close dropdown on click outside
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Filtered matching items
  const { matchingTaluks, matchingStations, matchingRisks } = useMemo(() => {
    const q = searchQuery.trim().toLowerCase();

    // Matching taluks
    const taluks = TALUKS_INFO.filter((t) => {
      if (!q) return false;
      return (
        t.name.toLowerCase().includes(q) ||
        t.id.toLowerCase().includes(q) ||
        t.alias.toLowerCase().includes(q)
      );
    }).map((t) => {
      const count = stations.filter(
        (s) => s.block.toUpperCase() === t.id || s.tehsil.toUpperCase() === t.id
      ).length;
      return { ...t, count };
    });

    // Matching stations
    const matchedSts = stations.filter((s) => {
      if (!q) return false;
      return (
        s.name.toLowerCase().includes(q) ||
        s.village.toLowerCase().includes(q) ||
        s.block.toLowerCase().includes(q) ||
        s.tehsil.toLowerCase().includes(q)
      );
    }).slice(0, 8); // Top 8 station suggestions

    // Matching risks if query mentions risk words
    const risks: Risk[] = [];
    if (q) {
      if ("high".includes(q) || "critical".includes(q) || "severe".includes(q)) risks.push("High");
      if ("moderate".includes(q) || "medium".includes(q)) risks.push("Moderate");
      if ("low".includes(q) || "mild".includes(q)) risks.push("Low");
      if ("safe".includes(q) || "no depletion".includes(q) || "stable".includes(q)) risks.push("No Depletion");
    }

    return {
      matchingTaluks: taluks,
      matchingStations: matchedSts,
      matchingRisks: risks,
    };
  }, [stations, searchQuery]);

  const totalResults = matchingTaluks.length + matchingRisks.length + matchingStations.length;

  // Flattened items for keyboard navigation
  const flatItems = useMemo(() => {
    const items: Array<{ type: "taluk" | "risk" | "station"; data: any }> = [];
    matchingTaluks.forEach((t) => items.push({ type: "taluk", data: t }));
    matchingRisks.forEach((r) => items.push({ type: "risk", data: r }));
    matchingStations.forEach((s) => items.push({ type: "station", data: s }));
    return items;
  }, [matchingTaluks, matchingRisks, matchingStations]);

  // Handle keyboard events
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (!isOpen && (e.key === "ArrowDown" || e.key === "Enter")) {
      setIsOpen(true);
      return;
    }

    if (e.key === "ArrowDown") {
      e.preventDefault();
      setSelectedIndex((prev) => (prev + 1) % (flatItems.length || 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setSelectedIndex((prev) => (prev - 1 + (flatItems.length || 1)) % (flatItems.length || 1));
    } else if (e.key === "Enter") {
      e.preventDefault();
      if (flatItems[selectedIndex]) {
        executeSelection(flatItems[selectedIndex]);
      }
    } else if (e.key === "Escape") {
      setIsOpen(false);
      inputRef.current?.blur();
    }
  };

  const executeSelection = (item: { type: "taluk" | "risk" | "station"; data: any }) => {
    if (item.type === "taluk") {
      onSelectTaluk(item.data.id);
      onSearchChange(item.data.name);
    } else if (item.type === "risk") {
      if (onSelectRisk) onSelectRisk(item.data);
      onSearchChange(item.data);
    } else if (item.type === "station") {
      onSelectStation(item.data);
      onSearchChange(item.data.name);
    }
    setIsOpen(false);
  };

  // Helper: Highlight matching text
  const highlightMatch = (text: string, query: string) => {
    if (!query.trim()) return text;
    const parts = text.split(new RegExp(`(${query.trim()})`, "gi"));
    return (
      <span>
        {parts.map((part, i) =>
          part.toLowerCase() === query.trim().toLowerCase() ? (
            <mark key={i} className="search-highlight">
              {part}
            </mark>
          ) : (
            part
          )
        )}
      </span>
    );
  };

  return (
    <div ref={containerRef} className={`smart-search-wrapper ${className}`}>
      <div className="smart-search-input-box">
        <Search size={17} className="smart-search-icon" />
        <input
          ref={inputRef}
          type="text"
          placeholder="Smart Search: Type station (e.g. Bilikere), taluk (Hunsur), or risk (High)..."
          value={searchQuery}
          onChange={(e) => {
            onSearchChange(e.target.value);
            setIsOpen(true);
            setSelectedIndex(0);
          }}
          onFocus={() => setIsOpen(true)}
          onKeyDown={handleKeyDown}
          className="smart-search-input"
        />

        {searchQuery && (
          <button
            type="button"
            className="smart-search-clear-btn"
            onClick={() => {
              onSearchChange("");
              setIsOpen(false);
              inputRef.current?.focus();
            }}
            title="Clear search"
          >
            <X size={15} />
          </button>
        )}

        <kbd className="search-kbd-hint">⌘K</kbd>
      </div>

      {/* AUTOCOMPLETE POPOVER */}
      {isOpen && (
        <div className="smart-search-popover">
          {totalResults === 0 && searchQuery.trim() ? (
            <div className="search-no-results">
              <p>No stations, taluks, or records found matching "<strong>{searchQuery}</strong>"</p>
              <div className="search-suggestions-hint">
                <span>Try searching:</span>
                <button type="button" onClick={() => { onSearchChange("Hunsur"); onSelectTaluk("HUNSUR"); setIsOpen(false); }}>Hunsur</button>
                <button type="button" onClick={() => { onSearchChange("Mysuru"); onSelectTaluk("MYSORE"); setIsOpen(false); }}>Mysuru</button>
                <button type="button" onClick={() => { onSearchChange("High"); if (onSelectRisk) onSelectRisk("High"); setIsOpen(false); }}>High Risk</button>
                <button type="button" onClick={() => { onSearchChange("Nanjangud"); onSelectTaluk("NANJANGUD"); setIsOpen(false); }}>Nanjangud</button>
              </div>
            </div>
          ) : null}

          {/* QUICK SUGGESTIONS IF QUERY IS EMPTY */}
          {!searchQuery.trim() && (
            <div className="search-quick-section">
              <div className="search-section-header">
                <Sparkles size={13} className="text-cyan" />
                <span>POPULAR MYSURU TALUKS</span>
              </div>
              <div className="search-quick-pills">
                {TALUKS_INFO.slice(0, 6).map((t) => {
                  const count = stations.filter(
                    (s) => s.block.toUpperCase() === t.id || s.tehsil.toUpperCase() === t.id
                  ).length;
                  return (
                    <button
                      key={t.id}
                      type="button"
                      className="quick-taluk-pill"
                      onClick={() => {
                        onSelectTaluk(t.id);
                        onSearchChange(t.name);
                        setIsOpen(false);
                      }}
                    >
                      <MapIcon size={12} />
                      <span>{t.name}</span>
                      <small className="pill-count">({count})</small>
                    </button>
                  );
                })}
              </div>

              <div className="search-section-header mt-2">
                <ShieldAlert size={13} className="text-amber" />
                <span>QUICK RISK SHORTCUTS</span>
              </div>
              <div className="search-quick-pills">
                {(["High", "Moderate", "Low", "No Depletion"] as Risk[]).map((r) => {
                  const rCount = stations.filter((s) => s.risk === r).length;
                  const badge = RISK_BADGES[r];
                  return (
                    <button
                      key={r}
                      type="button"
                      className="quick-risk-pill"
                      style={{ color: badge.color, borderColor: badge.color }}
                      onClick={() => {
                        if (onSelectRisk) onSelectRisk(r);
                        onSearchChange(r);
                        setIsOpen(false);
                      }}
                    >
                      <span className="dot" style={{ background: badge.color }} />
                      <span>{badge.label}</span>
                      <small>({rCount})</small>
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* MATCHING TALUKS */}
          {matchingTaluks.length > 0 && (
            <div className="search-group">
              <div className="search-group-title">
                <MapIcon size={12} />
                <span>ADMINISTRATIVE TALUKS ({matchingTaluks.length})</span>
              </div>
              {matchingTaluks.map((t, idx) => {
                const isSelected = flatItems[selectedIndex]?.data?.id === t.id;
                return (
                  <div
                    key={t.id}
                    className={`search-result-row ${isSelected ? "selected" : ""}`}
                    onClick={() => executeSelection({ type: "taluk", data: t })}
                    onMouseEnter={() => setSelectedIndex(idx)}
                  >
                    <div className="search-icon-cell taluk-icon">
                      <MapIcon size={15} />
                    </div>
                    <div className="search-text-cell">
                      <div className="title-row">
                        <span className="main-name">{highlightMatch(t.name, searchQuery)} Taluk</span>
                        <span className="badge-count">{t.count} CGWB Stations</span>
                      </div>
                      <small className="sub-text">Filter map and telemetry to {t.name} administrative boundary</small>
                    </div>
                    <ChevronRight size={14} className="arrow-hint" />
                  </div>
                );
              })}
            </div>
          )}

          {/* MATCHING RISKS */}
          {matchingRisks.length > 0 && (
            <div className="search-group">
              <div className="search-group-title">
                <ShieldAlert size={12} />
                <span>RISK CLASSIFICATIONS</span>
              </div>
              {matchingRisks.map((r) => {
                const badge = RISK_BADGES[r];
                const count = stations.filter((s) => s.risk === r).length;
                return (
                  <div
                    key={r}
                    className="search-result-row"
                    onClick={() => executeSelection({ type: "risk", data: r })}
                  >
                    <div className="search-icon-cell" style={{ background: badge.bg, color: badge.color }}>
                      <ShieldAlert size={15} />
                    </div>
                    <div className="search-text-cell">
                      <div className="title-row">
                        <span className="main-name" style={{ color: badge.color }}>Filter all {badge.label} Stations</span>
                        <span className="badge-count" style={{ borderColor: badge.color }}>{count} stations</span>
                      </div>
                      <small className="sub-text">Show stations with {r} depletion risk tier</small>
                    </div>
                    <ChevronRight size={14} className="arrow-hint" />
                  </div>
                );
              })}
            </div>
          )}

          {/* MATCHING STATIONS */}
          {matchingStations.length > 0 && (
            <div className="search-group">
              <div className="search-group-title">
                <MapPin size={12} />
                <span>MONITORING WELLS ({matchingStations.length})</span>
              </div>
              {matchingStations.map((st) => {
                const badge = RISK_BADGES[st.risk] || RISK_BADGES["Low"];
                const isSelected = flatItems[selectedIndex]?.data?.name === st.name;
                return (
                  <div
                    key={st.name}
                    className={`search-result-row ${isSelected ? "selected" : ""}`}
                    onClick={() => executeSelection({ type: "station", data: st })}
                  >
                    <div className="search-icon-cell station-icon" style={{ borderColor: badge.color }}>
                      <MapPin size={15} style={{ color: badge.color }} />
                    </div>
                    <div className="search-text-cell">
                      <div className="title-row">
                        <span className="main-name">{highlightMatch(st.name, searchQuery)}</span>
                        <span className="mini-risk-pill" style={{ color: badge.color, background: badge.bg }}>
                          {st.risk}
                        </span>
                      </div>
                      <div className="station-meta-row">
                        <span>Block: <strong>{highlightMatch(st.block, searchQuery)}</strong></span>
                        <span>•</span>
                        <span>Village: {highlightMatch(st.village, searchQuery)}</span>
                        <span>•</span>
                        <span>Current: <strong>{st.current.toFixed(2)}m</strong></span>
                        <span>•</span>
                        <span>Forecast: <strong>{st.predicted.toFixed(2)}m</strong></span>
                      </div>
                    </div>
                    <ChevronRight size={14} className="arrow-hint" />
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
