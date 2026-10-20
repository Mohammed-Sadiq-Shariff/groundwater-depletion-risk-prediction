import React from "react";
import {
  Filter,
  RotateCcw,
  MapPin,
  ShieldAlert,
  Droplets,
  TrendingDown,
  TrendingUp,
  X,
  Layers,
  Check,
} from "lucide-react";
import { Risk } from "../types/dashboard";

export interface FilterState {
  selectedTaluks: string[]; // empty means all
  selectedRisks: Risk[]; // empty means all
  depthRange: "all" | "shallow" | "medium" | "deep";
  trend: "all" | "depleting" | "improving";
}

interface MultiFilterBarProps {
  filters: FilterState;
  onChangeFilters: (newFilters: FilterState) => void;
  totalStations: number;
  matchingCount: number;
  availableTaluks: Array<{ id: string; name: string; count: number }>;
}

const RISK_CONFIG: Array<{ risk: Risk; label: string; color: string; bg: string }> = [
  { risk: "High", label: "High Risk", color: "#ef4444", bg: "rgba(239, 68, 68, 0.14)" },
  { risk: "Moderate", label: "Moderate", color: "#f59e0b", bg: "rgba(245, 158, 11, 0.14)" },
  { risk: "Low", label: "Low Risk", color: "#eab308", bg: "rgba(234, 179, 8, 0.14)" },
  { risk: "No Depletion", label: "Safe / Stable", color: "#10b981", bg: "rgba(16, 185, 129, 0.14)" },
];

export const MultiFilterBar: React.FC<MultiFilterBarProps> = ({
  filters,
  onChangeFilters,
  totalStations,
  matchingCount,
  availableTaluks,
}) => {
  // Toggle a taluk in multi-selection
  const toggleTaluk = (talukId: string) => {
    if (talukId === "ALL") {
      onChangeFilters({ ...filters, selectedTaluks: [] });
      return;
    }

    const current = [...filters.selectedTaluks];
    const index = current.indexOf(talukId);
    if (index >= 0) {
      current.splice(index, 1);
    } else {
      current.push(talukId);
    }
    onChangeFilters({ ...filters, selectedTaluks: current });
  };

  // Toggle a risk in multi-selection
  const toggleRisk = (risk: Risk) => {
    const current = [...filters.selectedRisks];
    const index = current.indexOf(risk);
    if (index >= 0) {
      current.splice(index, 1);
    } else {
      current.push(risk);
    }
    onChangeFilters({ ...filters, selectedRisks: current });
  };

  // Set depth range
  const setDepth = (depth: FilterState["depthRange"]) => {
    onChangeFilters({ ...filters, depthRange: depth });
  };

  // Set trend
  const setTrend = (trend: FilterState["trend"]) => {
    onChangeFilters({ ...filters, trend: trend });
  };

  // Reset all
  const resetFilters = () => {
    onChangeFilters({
      selectedTaluks: [],
      selectedRisks: [],
      depthRange: "all",
      trend: "all",
    });
  };

  // Active filter count
  const activeCount =
    (filters.selectedTaluks.length > 0 ? 1 : 0) +
    (filters.selectedRisks.length > 0 ? 1 : 0) +
    (filters.depthRange !== "all" ? 1 : 0) +
    (filters.trend !== "all" ? 1 : 0);

  return (
    <div className="multi-filter-container">
      {/* FILTER TOP HEADER & KPI COUNTER */}
      <div className="filter-header-bar">
        <div className="filter-title-group">
          <Filter size={16} className="text-cyan" />
          <span className="filter-title">MIX-MATCH MULTI FILTERS</span>
          {activeCount > 0 && (
            <span className="active-filter-badge">{activeCount} ACTIVE</span>
          )}
        </div>

        <div className="filter-results-counter">
          <span>Showing</span>
          <b className="matching-num">{matchingCount}</b>
          <span>of</span>
          <b>{totalStations}</b>
          <span>monitoring wells</span>

          {activeCount > 0 && (
            <button
              type="button"
              className="reset-filters-btn"
              onClick={resetFilters}
              title="Reset all filters"
            >
              <RotateCcw size={13} />
              <span>Reset All</span>
            </button>
          )}
        </div>
      </div>

      {/* FILTER CONTROLS GRID */}
      <div className="filter-rows-grid">
        {/* ROW 1: TALUK MULTI-SELECT PILLS */}
        <div className="filter-row">
          <div className="filter-row-label">
            <MapPin size={13} />
            <span>TALUK / BLOCK:</span>
          </div>
          <div className="filter-pill-wrap">
            <button
              type="button"
              className={`filter-chip ${filters.selectedTaluks.length === 0 ? "active" : ""}`}
              onClick={() => toggleTaluk("ALL")}
            >
              <span>All 9 Taluks</span>
              <small>({totalStations})</small>
            </button>

            {availableTaluks.map((t) => {
              const isSelected = filters.selectedTaluks.includes(t.id);
              return (
                <button
                  key={t.id}
                  type="button"
                  className={`filter-chip ${isSelected ? "active" : ""}`}
                  onClick={() => toggleTaluk(t.id)}
                >
                  {isSelected && <Check size={12} className="check-icon" />}
                  <span>{t.name}</span>
                  <small>({t.count})</small>
                </button>
              );
            })}
          </div>
        </div>

        {/* ROW 2: RISK CATEGORY MULTI-SELECT */}
        <div className="filter-row">
          <div className="filter-row-label">
            <ShieldAlert size={13} />
            <span>DEPLETION RISK:</span>
          </div>
          <div className="filter-pill-wrap">
            {RISK_CONFIG.map(({ risk, label, color, bg }) => {
              const isSelected = filters.selectedRisks.includes(risk);
              return (
                <button
                  key={risk}
                  type="button"
                  className={`filter-chip risk-chip ${isSelected ? "active" : ""}`}
                  style={
                    isSelected
                      ? { background: bg, borderColor: color, color: color }
                      : {}
                  }
                  onClick={() => toggleRisk(risk)}
                >
                  <span
                    className="risk-dot"
                    style={{ background: color }}
                  />
                  <span>{label}</span>
                  {isSelected && <Check size={12} className="check-icon" />}
                </button>
              );
            })}
            {filters.selectedRisks.length > 0 && (
              <button
                type="button"
                className="clear-mini-btn"
                onClick={() => onChangeFilters({ ...filters, selectedRisks: [] })}
              >
                Clear Risk
              </button>
            )}
          </div>
        </div>

        {/* ROW 3: WATER DEPTH & TREND */}
        <div className="filter-row dual-row">
          <div className="filter-subgroup">
            <div className="filter-row-label">
              <Droplets size={13} />
              <span>WATER TABLE DEPTH:</span>
            </div>
            <div className="filter-pill-wrap">
              <button
                type="button"
                className={`filter-chip ${filters.depthRange === "all" ? "active" : ""}`}
                onClick={() => setDepth("all")}
              >
                All Depths
              </button>
              <button
                type="button"
                className={`filter-chip ${filters.depthRange === "shallow" ? "active" : ""}`}
                onClick={() => setDepth("shallow")}
              >
                Shallow (&lt; 5m)
              </button>
              <button
                type="button"
                className={`filter-chip ${filters.depthRange === "medium" ? "active" : ""}`}
                onClick={() => setDepth("medium")}
              >
                Medium (5 - 12m)
              </button>
              <button
                type="button"
                className={`filter-chip ${filters.depthRange === "deep" ? "active" : ""}`}
                onClick={() => setDepth("deep")}
              >
                Deep (&gt; 12m)
              </button>
            </div>
          </div>

          <div className="filter-subgroup">
            <div className="filter-row-label">
              <TrendingDown size={13} />
              <span>PROJECTED TREND:</span>
            </div>
            <div className="filter-pill-wrap">
              <button
                type="button"
                className={`filter-chip ${filters.trend === "all" ? "active" : ""}`}
                onClick={() => setTrend("all")}
              >
                All Trends
              </button>
              <button
                type="button"
                className={`filter-chip trend-depleting ${filters.trend === "depleting" ? "active" : ""}`}
                onClick={() => setTrend("depleting")}
              >
                <TrendingUp size={12} className="text-red" />
                <span>Depleting (&gt; 0m)</span>
              </button>
              <button
                type="button"
                className={`filter-chip trend-improving ${filters.trend === "improving" ? "active" : ""}`}
                onClick={() => setTrend("improving")}
              >
                <TrendingDown size={12} className="text-green" />
                <span>Stable / Recovering</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* ACTIVE FILTER SUMMARY CHIPS */}
      {activeCount > 0 && (
        <div className="active-chips-tray">
          <span className="tray-label">Active Filters:</span>
          {filters.selectedTaluks.map((tid) => {
            const t = availableTaluks.find((x) => x.id === tid);
            return (
              <span key={tid} className="active-tag-chip">
                <span>Taluk: {t?.name || tid}</span>
                <button type="button" onClick={() => toggleTaluk(tid)}>
                  <X size={11} />
                </button>
              </span>
            );
          })}
          {filters.selectedRisks.map((r) => (
            <span key={r} className="active-tag-chip risk">
              <span>Risk: {r}</span>
              <button type="button" onClick={() => toggleRisk(r)}>
                <X size={11} />
              </button>
            </span>
          ))}
          {filters.depthRange !== "all" && (
            <span className="active-tag-chip">
              <span>Depth: {filters.depthRange}</span>
              <button type="button" onClick={() => setDepth("all")}>
                <X size={11} />
              </button>
            </span>
          )}
          {filters.trend !== "all" && (
            <span className="active-tag-chip">
              <span>Trend: {filters.trend}</span>
              <button type="button" onClick={() => setTrend("all")}>
                <X size={11} />
              </button>
            </span>
          )}
        </div>
      )}
    </div>
  );
};
