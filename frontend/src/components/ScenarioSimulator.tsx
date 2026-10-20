import React from "react";
import { CloudRain, Gauge, RotateCcw, AlertTriangle, ShieldCheck, Flame } from "lucide-react";

interface ScenarioSimulatorProps {
  rainfallAnomaly: number;
  setRainfallAnomaly: (val: number) => void;
  extractionStress: number;
  setExtractionStress: (val: number) => void;
  onReset: () => void;
}

export const ScenarioSimulator: React.FC<ScenarioSimulatorProps> = ({
  rainfallAnomaly,
  setRainfallAnomaly,
  extractionStress,
  setExtractionStress,
  onReset,
}) => {
  const isDrought = rainfallAnomaly < -20;
  const isSevere = rainfallAnomaly < -35 || extractionStress > 60;
  const isSurplus = rainfallAnomaly > 20;

  return (
    <div className="scenario-simulator-panel">
      <div className="sim-header">
        <div className="sim-title">
          <Gauge size={17} className="text-teal" />
          <b>LIVE STRESS-TEST SCENARIO SIMULATOR</b>
        </div>
        <div className="sim-actions">
          {(rainfallAnomaly !== 0 || extractionStress !== 0) && (
            <button type="button" className="sim-reset-btn" onClick={onReset}>
              <RotateCcw size={13} />
              <span>Reset Baseline</span>
            </button>
          )}
        </div>
      </div>

      <div className="sim-sliders-grid">
        {/* SLIDER 1: MONSOON RAINFALL DEVIATION */}
        <div className="sim-slider-box">
          <div className="slider-label-row">
            <span>
              <CloudRain size={15} /> Monsoon Rainfall Anomaly
            </span>
            <b
              className={
                rainfallAnomaly > 0
                  ? "text-success"
                  : rainfallAnomaly < 0
                  ? "text-danger"
                  : "text-muted"
              }
            >
              {rainfallAnomaly > 0 ? `+${rainfallAnomaly}% (Surplus)` : rainfallAnomaly < 0 ? `${rainfallAnomaly}% (Deficit)` : "0% (Normal Baseline)"}
            </b>
          </div>
          <input
            type="range"
            min="-50"
            max="50"
            step="5"
            value={rainfallAnomaly}
            onChange={(e) => setRainfallAnomaly(Number(e.target.value))}
            className="slider-input rain-slider"
          />
          <div className="slider-scale">
            <span>-50% Extreme Drought</span>
            <span>0% Normal</span>
            <span>+50% Heavy Monsoon</span>
          </div>
        </div>

        {/* SLIDER 2: AGRICULTURAL EXTRACTION INTENSITY */}
        <div className="sim-slider-box">
          <div className="slider-label-row">
            <span>
              <Flame size={15} /> Pumping Extraction Stress
            </span>
            <b className={extractionStress > 40 ? "text-danger" : extractionStress > 15 ? "text-amber" : "text-muted"}>
              +{extractionStress}% Above Normal
            </b>
          </div>
          <input
            type="range"
            min="0"
            max="100"
            step="10"
            value={extractionStress}
            onChange={(e) => setExtractionStress(Number(e.target.value))}
            className="slider-input extraction-slider"
          />
          <div className="slider-scale">
            <span>Normal Pumping</span>
            <span>+50% High Irrigation</span>
            <span>+100% Emergency Pumping</span>
          </div>
        </div>
      </div>

      {/* CLIMATE IMPACT BANNER */}
      {(rainfallAnomaly !== 0 || extractionStress !== 0) && (
        <div className={`sim-feedback-banner ${isSevere ? "severe" : isDrought ? "warning" : "positive"}`}>
          {isSevere ? (
            <AlertTriangle size={16} />
          ) : isSurplus ? (
            <ShieldCheck size={16} />
          ) : (
            <CloudRain size={16} />
          )}
          <span>
            {isSevere
              ? "Critical Warning: Compound climate drought and elevated extraction triggers accelerated aquifer decline. Multiple stations transition to High Depletion Risk."
              : isDrought
              ? "Monsoon deficit detected. Water table projected to deepen across central and western Mysuru taluks."
              : isSurplus
              ? "Surplus precipitation provides substantial aquifer replenishment. Net groundwater recharge rates improve across all taluks."
              : "Hydrological scenario simulated. Station predictions and choropleth risk classifications updated dynamically."}
          </span>
        </div>
      )}
    </div>
  );
};
