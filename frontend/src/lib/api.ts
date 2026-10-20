const API_BASE_URL = "";

type ApiEnvelope<T> = {
  value?: T;
  Count?: number;
};

export async function fetchAPI<T>(
  endpoint: string,
  options?: RequestInit,
): Promise<T> {
  const url = endpoint.startsWith("http") ? endpoint : `${API_BASE_URL}${endpoint}`;
  const response = await fetch(url, options);

  if (!response.ok) {
    const message = await response.text();
    throw new Error(
      `API request failed: ${response.status} ${response.statusText}${
        message ? ` - ${message}` : ""
      }`,
    );
  }

  const data = await response.json();

  if (data && typeof data === "object" && "value" in data) {
    return (data as ApiEnvelope<T>).value as T;
  }

  return data as T;
}

export const api = {
  health: () => fetchAPI("/api/health"),
  overview: () => fetchAPI("/api/dashboard/overview"),
  dashboard: () => fetchAPI("/api/dashboard"),
  stations: () => fetchAPI("/api/stations"),
  stationDetails: (stationName: string) =>
    fetchAPI(`/api/stations/${encodeURIComponent(stationName)}`),
  stationHistory: (stationName: string) =>
    fetchAPI(`/api/stations/${encodeURIComponent(stationName)}/history`),
  blocks: () => fetchAPI("/api/blocks"),
  predictions: () => fetchAPI("/api/predictions"),
  latestPredictions: () => fetchAPI("/api/predictions/latest"),
  riskDistribution: () => fetchAPI("/api/analytics/risk-distribution"),
  features: () => fetchAPI("/api/analytics/features"),

  // New GIS & Boundary endpoints
  boundariesTaluks: () => fetchAPI("/api/boundaries/taluks"),
  boundariesDistrict: () => fetchAPI("/api/boundaries/district"),

  // New Report & Export endpoints
  mapReport: () => fetchAPI("/api/reports/map"),
  getTemplateUrl: () => `${API_BASE_URL}/api/data/template`,
  getReportExcelUrl: () => `${API_BASE_URL}/api/reports/excel`,

  // Upload endpoint
  uploadData: async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    return fetchAPI<any>("/api/data/upload", {
      method: "POST",
      body: formData,
    });
  },
};