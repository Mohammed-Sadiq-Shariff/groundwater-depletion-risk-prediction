// Real Station Data & Historical Records from Mysore Groundwater Dataset
export interface StationRecord {
  name: string;
  district: string;
  tehsil: string;
  block: string;
  village: string;
  latitude: number;
  longitude: number;
  monitoringDate: string;
  current: number;
  predicted: number;
  change: number;
  risk: "No Depletion" | "Low" | "Moderate" | "High";
  probabilities: {
    no: number;
    low: number;
    moderate: number;
    high: number;
  };
  history: Array<{ date: string; level: number }>;
}

export const REAL_STATIONS: StationRecord[] = [
  {
    "name": "Airige",
    "district": "Mysore",
    "tehsil": "HEGGADADEVANKOTE",
    "block": "HEGGADADEVANKOTE",
    "village": "Hyrige",
    "latitude": 12.0,
    "longitude": 76.391667,
    "monitoringDate": "2009-11-05",
    "current": 15.91,
    "predicted": 15.27,
    "change": -0.64,
    "risk": "No Depletion",
    "probabilities": {
      "no": 30.8,
      "low": 23.1,
      "moderate": 23.2,
      "high": 22.9
    },
    "history": [
      {
        "date": "2004-05-11",
        "level": 7.28
      },
      {
        "date": "2005-05-01",
        "level": 7.93
      },
      {
        "date": "nan",
        "level": 8.72
      },
      {
        "date": "2006-05-11",
        "level": 15.91
      },
      {
        "date": "nan",
        "level": 15.91
      },
      {
        "date": "2007-05-11",
        "level": 15.91
      },
      {
        "date": "nan",
        "level": 15.91
      },
      {
        "date": "2009-05-11",
        "level": 15.91
      }
    ]
  },
  {
    "name": "Alaguda",
    "district": "Mysore",
    "tehsil": "TIRUMAKUDAL-NARSIPUR",
    "block": "TIRUMAKUDAL-NARSIPUR",
    "village": "Alaguda",
    "latitude": 12.201944,
    "longitude": 76.910556,
    "monitoringDate": "2024-01-05",
    "current": 2.75,
    "predicted": 3.48,
    "change": 0.73,
    "risk": "Low",
    "probabilities": {
      "no": 19.6,
      "low": 38.5,
      "moderate": 25.5,
      "high": 16.3
    },
    "history": [
      {
        "date": "nan",
        "level": 2.3
      },
      {
        "date": "nan",
        "level": 1.32
      },
      {
        "date": "nan",
        "level": 1.4
      },
      {
        "date": "2022-05-11",
        "level": 1.25
      },
      {
        "date": "2023-05-01",
        "level": 2.4
      },
      {
        "date": "nan",
        "level": 2.75
      },
      {
        "date": "nan",
        "level": 3.25
      },
      {
        "date": "2024-05-01",
        "level": 2.75
      }
    ]
  },
  {
    "name": "Allampur",
    "district": "Mysore",
    "tehsil": "NANJANGUD",
    "block": "NANJANGUD",
    "village": "Allampur",
    "latitude": 12.130833,
    "longitude": 76.74,
    "monitoringDate": "2024-01-05",
    "current": 4.0,
    "predicted": 4.23,
    "change": 0.23,
    "risk": "Moderate",
    "probabilities": {
      "no": 27.5,
      "low": 23.0,
      "moderate": 31.0,
      "high": 18.4
    },
    "history": [
      {
        "date": "nan",
        "level": 2.29
      },
      {
        "date": "nan",
        "level": 2.25
      },
      {
        "date": "2022-05-11",
        "level": 1.75
      },
      {
        "date": "2023-05-01",
        "level": 3.85
      },
      {
        "date": "nan",
        "level": 3.46
      },
      {
        "date": "nan",
        "level": 2.5
      },
      {
        "date": "2023-05-11",
        "level": 1.83
      },
      {
        "date": "2024-05-01",
        "level": 4.0
      }
    ]
  },
  {
    "name": "Anechowkur",
    "district": "Mysore",
    "tehsil": "HUNSUR",
    "block": "HUNSUR",
    "village": "Anechowkur Forest",
    "latitude": 12.313889,
    "longitude": 76.452778,
    "monitoringDate": "2023-08-25",
    "current": 6.5,
    "predicted": 5.48,
    "change": -1.02,
    "risk": "No Depletion",
    "probabilities": {
      "no": 39.3,
      "low": 17.3,
      "moderate": 38.9,
      "high": 4.5
    },
    "history": [
      {
        "date": "nan",
        "level": 2.08
      },
      {
        "date": "nan",
        "level": 4.08
      },
      {
        "date": "nan",
        "level": 5.73
      },
      {
        "date": "nan",
        "level": 1.83
      },
      {
        "date": "2022-05-11",
        "level": 2.33
      },
      {
        "date": "2023-05-01",
        "level": 5.75
      },
      {
        "date": "nan",
        "level": 7.65
      },
      {
        "date": "nan",
        "level": 6.5
      }
    ]
  },
  {
    "name": "Attigod",
    "district": "Mysore",
    "tehsil": "PIRIYAPATNA",
    "block": "PIRIYAPATNA",
    "village": "Attigod",
    "latitude": 12.491667,
    "longitude": 76.136111,
    "monitoringDate": "2022-05-25",
    "current": 16.1,
    "predicted": 14.1,
    "change": -2.0,
    "risk": "No Depletion",
    "probabilities": {
      "no": 63.0,
      "low": 10.8,
      "moderate": 15.8,
      "high": 10.4
    },
    "history": [
      {
        "date": "nan",
        "level": 23.5
      },
      {
        "date": "2020-10-01",
        "level": 8.01
      },
      {
        "date": "nan",
        "level": 18.8
      },
      {
        "date": "2021-10-01",
        "level": 23.5
      },
      {
        "date": "nan",
        "level": 23.5
      },
      {
        "date": "nan",
        "level": 4.99
      },
      {
        "date": "nan",
        "level": 16.15
      },
      {
        "date": "nan",
        "level": 16.1
      }
    ]
  },
  {
    "name": "Badakanakoppalu",
    "district": "Mysore",
    "tehsil": "KRISHNARAJANAGARA",
    "block": "KRISHNARAJANAGARA",
    "village": "Badakanakoppalu",
    "latitude": 12.511389,
    "longitude": 76.389722,
    "monitoringDate": "2024-01-05",
    "current": 7.1,
    "predicted": 9.39,
    "change": 2.29,
    "risk": "High",
    "probabilities": {
      "no": 19.3,
      "low": 10.7,
      "moderate": 21.8,
      "high": 48.2
    },
    "history": [
      {
        "date": "nan",
        "level": 1.85
      },
      {
        "date": "nan",
        "level": 3.68
      },
      {
        "date": "2022-05-11",
        "level": 2.95
      },
      {
        "date": "2023-05-01",
        "level": 7.05
      },
      {
        "date": "nan",
        "level": 10.9
      },
      {
        "date": "nan",
        "level": 8.9
      },
      {
        "date": "2023-05-11",
        "level": 7.02
      },
      {
        "date": "2024-05-01",
        "level": 7.1
      }
    ]
  },
  {
    "name": "Bannur",
    "district": "Mysore",
    "tehsil": "TIRUMAKUDAL-NARSIPUR",
    "block": "TIRUMAKUDAL-NARSIPUR",
    "village": "Bannur",
    "latitude": 12.316667,
    "longitude": 76.85,
    "monitoringDate": "2024-01-05",
    "current": 4.5,
    "predicted": 6.21,
    "change": 1.71,
    "risk": "Low",
    "probabilities": {
      "no": 23.4,
      "low": 28.4,
      "moderate": 24.7,
      "high": 23.5
    },
    "history": [
      {
        "date": "nan",
        "level": 1.33
      },
      {
        "date": "nan",
        "level": 3.52
      },
      {
        "date": "nan",
        "level": 2.05
      },
      {
        "date": "2022-05-11",
        "level": 1.62
      },
      {
        "date": "nan",
        "level": 3.59
      },
      {
        "date": "nan",
        "level": 4.52
      },
      {
        "date": "2023-05-11",
        "level": 4.61
      },
      {
        "date": "2024-05-01",
        "level": 4.5
      }
    ]
  },
  {
    "name": "Bannur A",
    "district": "Mysore",
    "tehsil": "TIRUMAKUDAL-NARSIPUR",
    "block": "-",
    "village": "-",
    "latitude": 12.33,
    "longitude": 76.8625,
    "monitoringDate": "2024-01-05",
    "current": 8.6,
    "predicted": 8.39,
    "change": -0.21,
    "risk": "No Depletion",
    "probabilities": {
      "no": 28.6,
      "low": 20.9,
      "moderate": 25.7,
      "high": 24.8
    },
    "history": [
      {
        "date": "nan",
        "level": 5.8
      },
      {
        "date": "nan",
        "level": 7.05
      },
      {
        "date": "2014-05-11",
        "level": 4.0
      },
      {
        "date": "2015-05-01",
        "level": 4.2
      },
      {
        "date": "nan",
        "level": 7.1
      },
      {
        "date": "nan",
        "level": 8.38
      },
      {
        "date": "nan",
        "level": 9.5
      },
      {
        "date": "2024-05-01",
        "level": 8.6
      }
    ]
  },
  {
    "name": "Bannur1",
    "district": "Mysore",
    "tehsil": "TIRUMAKUDAL-NARSIPUR",
    "block": "TIRUMAKUDAL-NARSIPUR",
    "village": "Bannur",
    "latitude": 12.316667,
    "longitude": 76.838889,
    "monitoringDate": "2010-05-15",
    "current": 2.48,
    "predicted": 2.6,
    "change": 0.12,
    "risk": "No Depletion",
    "probabilities": {
      "no": 45.5,
      "low": 35.0,
      "moderate": 15.9,
      "high": 3.5
    },
    "history": [
      {
        "date": "2002-05-01",
        "level": 2.66
      },
      {
        "date": "nan",
        "level": 6.09
      },
      {
        "date": "2002-05-11",
        "level": 1.6
      },
      {
        "date": "nan",
        "level": 2.48
      },
      {
        "date": "2004-05-11",
        "level": 1.46
      },
      {
        "date": "2005-05-01",
        "level": 2.05
      },
      {
        "date": "nan",
        "level": 3.77
      },
      {
        "date": "nan",
        "level": 2.48
      }
    ]
  },
  {
    "name": "Beemanahalli",
    "district": "Mysore",
    "tehsil": "HEGGADADEVANKOTE",
    "block": "HEGGADADEVANKOTE",
    "village": "Beemanahalli",
    "latitude": 12.183333,
    "longitude": 76.275,
    "monitoringDate": "2013-05-15",
    "current": 18.83,
    "predicted": 12.95,
    "change": -5.88,
    "risk": "No Depletion",
    "probabilities": {
      "no": 70.9,
      "low": 10.6,
      "moderate": 9.1,
      "high": 9.4
    },
    "history": [
      {
        "date": "2012-05-11",
        "level": 4.8
      },
      {
        "date": "2013-05-01",
        "level": 18.83
      },
      {
        "date": "nan",
        "level": 18.83
      }
    ]
  },
  {
    "name": "Beeredevanapura",
    "district": "Mysore",
    "tehsil": "NANJANGUD",
    "block": "NANJANGUD",
    "village": "Beeredevanapura",
    "latitude": 11.933611,
    "longitude": 76.525833,
    "monitoringDate": "2024-01-05",
    "current": 6.88,
    "predicted": 7.74,
    "change": 0.86,
    "risk": "No Depletion",
    "probabilities": {
      "no": 31.0,
      "low": 22.5,
      "moderate": 27.0,
      "high": 19.5
    },
    "history": [
      {
        "date": "nan",
        "level": 6.62
      },
      {
        "date": "nan",
        "level": 1.1
      },
      {
        "date": "2022-05-11",
        "level": 6.45
      },
      {
        "date": "2023-05-01",
        "level": 2.7
      },
      {
        "date": "nan",
        "level": 2.8
      },
      {
        "date": "nan",
        "level": 3.0
      },
      {
        "date": "2023-05-11",
        "level": 2.52
      },
      {
        "date": "2024-05-01",
        "level": 6.88
      }
    ]
  },
  {
    "name": "Bettadapura",
    "district": "Mysore",
    "tehsil": "NANJANGUD",
    "block": "NANJANGUD",
    "village": "Bettadapura",
    "latitude": 12.091667,
    "longitude": 76.516667,
    "monitoringDate": "2024-01-05",
    "current": 5.65,
    "predicted": 10.89,
    "change": 5.24,
    "risk": "Moderate",
    "probabilities": {
      "no": 28.1,
      "low": 18.0,
      "moderate": 32.0,
      "high": 21.9
    },
    "history": [
      {
        "date": "2020-10-01",
        "level": 18.5
      },
      {
        "date": "nan",
        "level": 17.69
      },
      {
        "date": "2021-10-01",
        "level": 17.69
      },
      {
        "date": "nan",
        "level": 17.69
      },
      {
        "date": "nan",
        "level": 2.92
      },
      {
        "date": "2022-05-11",
        "level": 4.49
      },
      {
        "date": "nan",
        "level": 5.65
      },
      {
        "date": "2024-05-01",
        "level": 5.65
      }
    ]
  },
  {
    "name": "Bettdapura",
    "district": "Mysore",
    "tehsil": "PIRIYAPATNA",
    "block": "PIRIYAPATNA",
    "village": "Bettdapura",
    "latitude": 12.470833,
    "longitude": 76.108333,
    "monitoringDate": "2024-01-05",
    "current": 14.2,
    "predicted": 16.79,
    "change": 2.59,
    "risk": "High",
    "probabilities": {
      "no": 23.8,
      "low": 10.5,
      "moderate": 26.5,
      "high": 39.2
    },
    "history": [
      {
        "date": "nan",
        "level": 4.79
      },
      {
        "date": "nan",
        "level": 6.41
      },
      {
        "date": "nan",
        "level": 5.07
      },
      {
        "date": "2022-05-11",
        "level": 4.6
      },
      {
        "date": "2023-05-01",
        "level": 8.67
      },
      {
        "date": "nan",
        "level": 16.53
      },
      {
        "date": "nan",
        "level": 11.75
      },
      {
        "date": "2024-05-01",
        "level": 14.2
      }
    ]
  },
  {
    "name": "Bevinahalli",
    "district": "Mysore",
    "tehsil": "MYSORE",
    "block": "MYSORE",
    "village": "Bevinahalli",
    "latitude": 12.306667,
    "longitude": 76.885,
    "monitoringDate": "2024-01-05",
    "current": 2.34,
    "predicted": 6.01,
    "change": 3.67,
    "risk": "High",
    "probabilities": {
      "no": 20.9,
      "low": 26.9,
      "moderate": 20.6,
      "high": 31.6
    },
    "history": [
      {
        "date": "nan",
        "level": 1.35
      },
      {
        "date": "nan",
        "level": 1.3
      },
      {
        "date": "2022-05-11",
        "level": 1.4
      },
      {
        "date": "2023-05-01",
        "level": 2.95
      },
      {
        "date": "nan",
        "level": 3.08
      },
      {
        "date": "nan",
        "level": 2.5
      },
      {
        "date": "2023-05-11",
        "level": 7.48
      },
      {
        "date": "2024-05-01",
        "level": 2.34
      }
    ]
  },
  {
    "name": "Bheerya-A",
    "district": "Mysore",
    "tehsil": "KRISHNARAJANAGARA",
    "block": "KRISHNARAJANAGARA",
    "village": "Bheerya-A",
    "latitude": 12.5,
    "longitude": 76.269722,
    "monitoringDate": "2024-01-05",
    "current": 3.17,
    "predicted": 7.2,
    "change": 4.03,
    "risk": "High",
    "probabilities": {
      "no": 26.5,
      "low": 17.3,
      "moderate": 21.8,
      "high": 34.4
    },
    "history": [
      {
        "date": "nan",
        "level": 0.62
      },
      {
        "date": "nan",
        "level": 1.1
      },
      {
        "date": "2022-05-11",
        "level": 0.9
      },
      {
        "date": "2023-05-01",
        "level": 3.15
      },
      {
        "date": "nan",
        "level": 4.92
      },
      {
        "date": "nan",
        "level": 4.1
      },
      {
        "date": "2023-05-11",
        "level": 8.99
      },
      {
        "date": "2024-05-01",
        "level": 3.17
      }
    ]
  },
  {
    "name": "Bherya",
    "district": "Mysore",
    "tehsil": "KRISHNARAJANAGARA",
    "block": "KRISHNARAJANAGARA",
    "village": "Bherya",
    "latitude": 12.5,
    "longitude": 76.269444,
    "monitoringDate": "2013-05-15",
    "current": 13.98,
    "predicted": 11.8,
    "change": -2.18,
    "risk": "No Depletion",
    "probabilities": {
      "no": 57.7,
      "low": 18.1,
      "moderate": 9.6,
      "high": 14.7
    },
    "history": [
      {
        "date": "2010-05-01",
        "level": 4.34
      },
      {
        "date": "nan",
        "level": 6.23
      },
      {
        "date": "nan",
        "level": 6.45
      },
      {
        "date": "2010-05-11",
        "level": 3.7
      },
      {
        "date": "2011-05-01",
        "level": 3.17
      },
      {
        "date": "nan",
        "level": 15.11
      },
      {
        "date": "2011-05-11",
        "level": 5.91
      },
      {
        "date": "nan",
        "level": 13.98
      }
    ]
  },
  {
    "name": "Bilikere",
    "district": "Mysore",
    "tehsil": "HUNSUR",
    "block": "HUNSUR",
    "village": "Bilikere",
    "latitude": 12.283333,
    "longitude": 76.2875,
    "monitoringDate": "2013-05-15",
    "current": 11.66,
    "predicted": 10.61,
    "change": -1.05,
    "risk": "No Depletion",
    "probabilities": {
      "no": 70.3,
      "low": 10.0,
      "moderate": 11.3,
      "high": 8.3
    },
    "history": [
      {
        "date": "nan",
        "level": 11.66
      },
      {
        "date": "nan",
        "level": 11.66
      },
      {
        "date": "2011-05-11",
        "level": 11.66
      },
      {
        "date": "2012-05-01",
        "level": 11.66
      },
      {
        "date": "nan",
        "level": 11.66
      },
      {
        "date": "2012-05-11",
        "level": 11.66
      },
      {
        "date": "2013-05-01",
        "level": 11.66
      },
      {
        "date": "nan",
        "level": 11.66
      }
    ]
  },
  {
    "name": "Bylakuppe",
    "district": "Mysore",
    "tehsil": "PIRIYAPATNA",
    "block": "PIRIYAPATNA",
    "village": "Bylakuppe",
    "latitude": 12.491667,
    "longitude": 76.211111,
    "monitoringDate": "2024-01-05",
    "current": 3.9,
    "predicted": 8.55,
    "change": 4.65,
    "risk": "High",
    "probabilities": {
      "no": 20.1,
      "low": 21.9,
      "moderate": 21.4,
      "high": 36.7
    },
    "history": [
      {
        "date": "nan",
        "level": 2.91
      },
      {
        "date": "nan",
        "level": 1.74
      },
      {
        "date": "2022-05-11",
        "level": 2.22
      },
      {
        "date": "2023-05-01",
        "level": 4.3
      },
      {
        "date": "nan",
        "level": 4.4
      },
      {
        "date": "nan",
        "level": 3.6
      },
      {
        "date": "2023-05-11",
        "level": 4.1
      },
      {
        "date": "2024-05-01",
        "level": 3.9
      }
    ]
  },
  {
    "name": "Chamundibetta",
    "district": "Mysore",
    "tehsil": "KRISHNARAJANAGARA",
    "block": "KRISHNARAJANAGARA",
    "village": "Chamundibetta",
    "latitude": 12.5625,
    "longitude": 76.258611,
    "monitoringDate": "2023-08-25",
    "current": 3.0,
    "predicted": 3.39,
    "change": 0.39,
    "risk": "No Depletion",
    "probabilities": {
      "no": 59.5,
      "low": 25.7,
      "moderate": 6.8,
      "high": 7.9
    },
    "history": [
      {
        "date": "2021-10-01",
        "level": 9.87
      },
      {
        "date": "nan",
        "level": 3.29
      },
      {
        "date": "nan",
        "level": 3.59
      },
      {
        "date": "nan",
        "level": 3.29
      },
      {
        "date": "nan",
        "level": 3.49
      },
      {
        "date": "2022-05-11",
        "level": 3.29
      },
      {
        "date": "nan",
        "level": 4.1
      },
      {
        "date": "nan",
        "level": 3.0
      }
    ]
  },
  {
    "name": "Chikkahunsur",
    "district": "Mysore",
    "tehsil": "HUNSUR",
    "block": "HUNSUR",
    "village": "Chikkahunsur",
    "latitude": 12.395833,
    "longitude": 76.341667,
    "monitoringDate": "2006-11-05",
    "current": 8.78,
    "predicted": 7.61,
    "change": -1.17,
    "risk": "Moderate",
    "probabilities": {
      "no": 23.6,
      "low": 26.9,
      "moderate": 37.1,
      "high": 12.4
    },
    "history": [
      {
        "date": "2004-05-01",
        "level": 3.93
      },
      {
        "date": "nan",
        "level": 4.32
      },
      {
        "date": "nan",
        "level": 1.54
      },
      {
        "date": "2004-05-11",
        "level": 1.26
      },
      {
        "date": "2005-05-01",
        "level": 2.5
      },
      {
        "date": "nan",
        "level": 4.58
      },
      {
        "date": "2006-05-01",
        "level": 1.8
      },
      {
        "date": "2006-05-11",
        "level": 8.78
      }
    ]
  },
  {
    "name": "Chikkayyanachathra",
    "district": "Mysore",
    "tehsil": "NANJANGUD",
    "block": "NANJANGUD",
    "village": "Chikkayyanachathra",
    "latitude": 12.072222,
    "longitude": 76.683333,
    "monitoringDate": "2024-01-05",
    "current": 3.25,
    "predicted": 2.37,
    "change": -0.88,
    "risk": "No Depletion",
    "probabilities": {
      "no": 36.5,
      "low": 26.8,
      "moderate": 21.2,
      "high": 15.5
    },
    "history": [
      {
        "date": "nan",
        "level": 2.38
      },
      {
        "date": "nan",
        "level": 0.6
      },
      {
        "date": "2022-05-11",
        "level": 0.48
      },
      {
        "date": "2023-05-01",
        "level": 3.0
      },
      {
        "date": "nan",
        "level": 2.33
      },
      {
        "date": "nan",
        "level": 1.25
      },
      {
        "date": "2023-05-11",
        "level": 1.47
      },
      {
        "date": "2024-05-01",
        "level": 3.25
      }
    ]
  },
  {
    "name": "Chunchankatte",
    "district": "Mysore",
    "tehsil": "KRISHNARAJANAGARA",
    "block": "KRISHNARAJANAGARA",
    "village": "Chunchankatte",
    "latitude": 12.504167,
    "longitude": 76.291667,
    "monitoringDate": "2024-01-05",
    "current": 5.85,
    "predicted": 7.47,
    "change": 1.62,
    "risk": "Moderate",
    "probabilities": {
      "no": 25.9,
      "low": 20.0,
      "moderate": 28.8,
      "high": 25.3
    },
    "history": [
      {
        "date": "nan",
        "level": 4.18
      },
      {
        "date": "nan",
        "level": 1.2
      },
      {
        "date": "nan",
        "level": 3.85
      },
      {
        "date": "2022-05-11",
        "level": 3.0
      },
      {
        "date": "2023-05-01",
        "level": 4.3
      },
      {
        "date": "nan",
        "level": 4.83
      },
      {
        "date": "nan",
        "level": 3.47
      },
      {
        "date": "2024-05-01",
        "level": 5.85
      }
    ]
  },
  {
    "name": "Dallalu",
    "district": "Mysore",
    "tehsil": "HUNSUR",
    "block": "HUNSUR",
    "village": "Dallalu",
    "latitude": 12.291667,
    "longitude": 76.1625,
    "monitoringDate": "2005-05-15",
    "current": 5.96,
    "predicted": 4.23,
    "change": -1.73,
    "risk": "No Depletion",
    "probabilities": {
      "no": 63.2,
      "low": 18.2,
      "moderate": 13.5,
      "high": 5.2
    },
    "history": [
      {
        "date": "nan",
        "level": 3.02
      },
      {
        "date": "2003-05-11",
        "level": 1.21
      },
      {
        "date": "2004-05-01",
        "level": 3.9
      },
      {
        "date": "nan",
        "level": 5.66
      },
      {
        "date": "nan",
        "level": 3.22
      },
      {
        "date": "2004-05-11",
        "level": 2.34
      },
      {
        "date": "2005-05-01",
        "level": 3.83
      },
      {
        "date": "nan",
        "level": 5.96
      }
    ]
  },
  {
    "name": "Depuru",
    "district": "Mysore",
    "tehsil": "PIRIYAPATNA",
    "block": "PIRIYAPATNA",
    "village": "Depuru",
    "latitude": 12.4625,
    "longitude": 76.073056,
    "monitoringDate": "2024-01-05",
    "current": 4.8,
    "predicted": 10.14,
    "change": 5.34,
    "risk": "High",
    "probabilities": {
      "no": 21.4,
      "low": 22.4,
      "moderate": 21.9,
      "high": 34.3
    },
    "history": [
      {
        "date": "nan",
        "level": 3.07
      },
      {
        "date": "nan",
        "level": 1.5
      },
      {
        "date": "2022-05-11",
        "level": 1.87
      },
      {
        "date": "2023-05-01",
        "level": 6.1
      },
      {
        "date": "nan",
        "level": 5.77
      },
      {
        "date": "nan",
        "level": 5.11
      },
      {
        "date": "2023-05-11",
        "level": 5.06
      },
      {
        "date": "2024-05-01",
        "level": 4.8
      }
    ]
  },
  {
    "name": "Deveerammanahalli",
    "district": "Mysore",
    "tehsil": "MYSORE",
    "block": "MYSORE",
    "village": "Deveerammanahalli",
    "latitude": 12.266667,
    "longitude": 76.666667,
    "monitoringDate": "2023-01-05",
    "current": 3.18,
    "predicted": 4.39,
    "change": 1.21,
    "risk": "Low",
    "probabilities": {
      "no": 23.1,
      "low": 33.2,
      "moderate": 23.5,
      "high": 20.2
    },
    "history": [
      {
        "date": "nan",
        "level": 5.4
      },
      {
        "date": "2017-05-01",
        "level": 18.54
      },
      {
        "date": "nan",
        "level": 0.9
      },
      {
        "date": "2019-01-05",
        "level": 3.82
      },
      {
        "date": "nan",
        "level": 1.1
      },
      {
        "date": "nan",
        "level": 2.05
      },
      {
        "date": "2020-10-01",
        "level": 2.78
      },
      {
        "date": "2023-05-01",
        "level": 3.18
      }
    ]
  },
  {
    "name": "Deviramanahalli",
    "district": "Mysore",
    "tehsil": "NANJANGUD",
    "block": "NANJANGUD",
    "village": "Deviramanahalli",
    "latitude": 12.102778,
    "longitude": 76.677778,
    "monitoringDate": "2024-01-05",
    "current": 3.92,
    "predicted": 4.45,
    "change": 0.53,
    "risk": "No Depletion",
    "probabilities": {
      "no": 28.0,
      "low": 23.9,
      "moderate": 27.6,
      "high": 20.5
    },
    "history": [
      {
        "date": "nan",
        "level": 2.67
      },
      {
        "date": "nan",
        "level": 1.86
      },
      {
        "date": "nan",
        "level": 1.55
      },
      {
        "date": "2022-05-11",
        "level": 1.6
      },
      {
        "date": "nan",
        "level": 3.2
      },
      {
        "date": "nan",
        "level": 3.27
      },
      {
        "date": "2023-05-11",
        "level": 3.01
      },
      {
        "date": "2024-05-01",
        "level": 3.92
      }
    ]
  },
  {
    "name": "Elwala",
    "district": "Mysore",
    "tehsil": "TIRUMAKUDAL-NARSIPUR",
    "block": "TIRUMAKUDAL-NARSIPUR",
    "village": "Elwala",
    "latitude": 12.283333,
    "longitude": 76.883333,
    "monitoringDate": "2015-11-05",
    "current": 8.89,
    "predicted": 9.61,
    "change": 0.72,
    "risk": "No Depletion",
    "probabilities": {
      "no": 34.3,
      "low": 28.3,
      "moderate": 18.3,
      "high": 19.1
    },
    "history": [
      {
        "date": "2012-05-11",
        "level": 3.69
      },
      {
        "date": "2013-05-01",
        "level": 4.56
      },
      {
        "date": "nan",
        "level": 8.89
      },
      {
        "date": "nan",
        "level": 8.89
      },
      {
        "date": "nan",
        "level": 8.89
      },
      {
        "date": "2014-05-11",
        "level": 8.89
      },
      {
        "date": "2015-05-01",
        "level": 8.89
      },
      {
        "date": "2015-05-11",
        "level": 8.89
      }
    ]
  },
  {
    "name": "Gandhigrama",
    "district": "Mysore",
    "tehsil": "NANJANGUD",
    "block": "NANJANGUD",
    "village": "Gandhigrama",
    "latitude": 12.115278,
    "longitude": 76.601667,
    "monitoringDate": "2024-01-05",
    "current": 5.2,
    "predicted": 5.9,
    "change": 0.7,
    "risk": "Moderate",
    "probabilities": {
      "no": 30.1,
      "low": 15.4,
      "moderate": 32.4,
      "high": 22.1
    },
    "history": [
      {
        "date": "nan",
        "level": 3.22
      },
      {
        "date": "nan",
        "level": 2.37
      },
      {
        "date": "2022-05-11",
        "level": 2.52
      },
      {
        "date": "2023-05-01",
        "level": 5.25
      },
      {
        "date": "nan",
        "level": 5.85
      },
      {
        "date": "nan",
        "level": 3.9
      },
      {
        "date": "2023-05-11",
        "level": 1.46
      },
      {
        "date": "2024-05-01",
        "level": 5.2
      }
    ]
  },
  {
    "name": "Gargeswari",
    "district": "Mysore",
    "tehsil": "KRISHNARAJANAGARA",
    "block": "KRISHNARAJANAGARA",
    "village": "Gargeswari",
    "latitude": 12.5,
    "longitude": 76.35,
    "monitoringDate": "2023-08-25",
    "current": 3.5,
    "predicted": 4.18,
    "change": 0.68,
    "risk": "No Depletion",
    "probabilities": {
      "no": 63.0,
      "low": 17.8,
      "moderate": 10.2,
      "high": 9.0
    },
    "history": [
      {
        "date": "2020-10-01",
        "level": 2.15
      },
      {
        "date": "nan",
        "level": 7.12
      },
      {
        "date": "2021-10-01",
        "level": 12.75
      },
      {
        "date": "nan",
        "level": 12.75
      },
      {
        "date": "nan",
        "level": 6.11
      },
      {
        "date": "nan",
        "level": 9.45
      },
      {
        "date": "nan",
        "level": 6.64
      },
      {
        "date": "nan",
        "level": 3.5
      }
    ]
  },
  {
    "name": "Gowdagere",
    "district": "Mysore",
    "tehsil": "HUNSUR",
    "block": "HUNSUR",
    "village": "Gowdikere",
    "latitude": 12.191667,
    "longitude": 76.375,
    "monitoringDate": "2022-11-05",
    "current": 7.52,
    "predicted": 6.73,
    "change": -0.79,
    "risk": "Low",
    "probabilities": {
      "no": 21.1,
      "low": 35.8,
      "moderate": 29.8,
      "high": 13.4
    },
    "history": [
      {
        "date": "2020-10-01",
        "level": 1.56
      },
      {
        "date": "nan",
        "level": 8.07
      },
      {
        "date": "2021-10-01",
        "level": 8.27
      },
      {
        "date": "nan",
        "level": 7.24
      },
      {
        "date": "nan",
        "level": 8.32
      },
      {
        "date": "nan",
        "level": 5.17
      },
      {
        "date": "nan",
        "level": 7.57
      },
      {
        "date": "2022-05-11",
        "level": 7.52
      }
    ]
  },
  {
    "name": "Guluru",
    "district": "Mysore",
    "tehsil": "NANJANGUD",
    "block": "NANJANGUD",
    "village": "Guluru",
    "latitude": 12.111111,
    "longitude": 76.705556,
    "monitoringDate": "2024-01-05",
    "current": 2.4,
    "predicted": 3.25,
    "change": 0.85,
    "risk": "Moderate",
    "probabilities": {
      "no": 27.9,
      "low": 26.9,
      "moderate": 30.8,
      "high": 14.4
    },
    "history": [
      {
        "date": "nan",
        "level": 0.8
      },
      {
        "date": "nan",
        "level": 0.6
      },
      {
        "date": "2022-05-11",
        "level": 0.4
      },
      {
        "date": "2023-05-01",
        "level": 2.35
      },
      {
        "date": "nan",
        "level": 2.9
      },
      {
        "date": "nan",
        "level": 2.68
      },
      {
        "date": "2023-05-11",
        "level": 1.84
      },
      {
        "date": "2024-05-01",
        "level": 2.4
      }
    ]
  },
  {
    "name": "Hampapur",
    "district": "Mysore",
    "tehsil": "HEGGADADEVANKOTE",
    "block": "HEGGADADEVANKOTE",
    "village": "Hampapur",
    "latitude": 12.120833,
    "longitude": 76.466667,
    "monitoringDate": "2024-01-05",
    "current": 3.83,
    "predicted": 8.47,
    "change": 4.64,
    "risk": "High",
    "probabilities": {
      "no": 18.5,
      "low": 17.5,
      "moderate": 22.0,
      "high": 42.0
    },
    "history": [
      {
        "date": "nan",
        "level": 2.75
      },
      {
        "date": "nan",
        "level": 1.55
      },
      {
        "date": "2022-05-11",
        "level": 1.27
      },
      {
        "date": "2023-05-01",
        "level": 3.35
      },
      {
        "date": "nan",
        "level": 5.5
      },
      {
        "date": "nan",
        "level": 5.5
      },
      {
        "date": "2023-05-11",
        "level": 3.4
      },
      {
        "date": "2024-05-01",
        "level": 3.83
      }
    ]
  },
  {
    "name": "Hampapura",
    "district": "Mysore",
    "tehsil": "KRISHNARAJANAGARA",
    "block": "KRISHNARAJANAGARA",
    "village": "Hampapura",
    "latitude": 12.488889,
    "longitude": 76.4,
    "monitoringDate": "2013-08-25",
    "current": 4.2,
    "predicted": 2.76,
    "change": -1.44,
    "risk": "No Depletion",
    "probabilities": {
      "no": 65.5,
      "low": 24.8,
      "moderate": 7.3,
      "high": 2.4
    },
    "history": [
      {
        "date": "2013-05-01",
        "level": 2.3
      },
      {
        "date": "nan",
        "level": 4.2
      }
    ]
  },
  {
    "name": "Hampapura A",
    "district": "Mysore",
    "tehsil": "KRISHNARAJANAGARA",
    "block": "KRISHNARAJANAGARA",
    "village": "Hampapura",
    "latitude": 12.4925,
    "longitude": 76.397222,
    "monitoringDate": "2017-11-05",
    "current": 2.35,
    "predicted": 4.32,
    "change": 1.97,
    "risk": "Low",
    "probabilities": {
      "no": 18.4,
      "low": 40.9,
      "moderate": 25.0,
      "high": 15.7
    },
    "history": [
      {
        "date": "nan",
        "level": 3.23
      },
      {
        "date": "2014-05-11",
        "level": 3.1
      },
      {
        "date": "2015-05-01",
        "level": 4.04
      },
      {
        "date": "nan",
        "level": 4.83
      },
      {
        "date": "nan",
        "level": 5.1
      },
      {
        "date": "2015-05-11",
        "level": 1.3
      },
      {
        "date": "2016-05-01",
        "level": 2.15
      },
      {
        "date": "2017-05-11",
        "level": 2.35
      }
    ]
  },
  {
    "name": "Hanagodu",
    "district": "Mysore",
    "tehsil": "HEGGADADEVANKOTE",
    "block": "HEGGADADEVANKOTE",
    "village": "Hanagodu",
    "latitude": 12.141667,
    "longitude": 76.291667,
    "monitoringDate": "2024-01-05",
    "current": 1.69,
    "predicted": 7.8,
    "change": 6.11,
    "risk": "High",
    "probabilities": {
      "no": 18.3,
      "low": 21.3,
      "moderate": 26.0,
      "high": 34.4
    },
    "history": [
      {
        "date": "nan",
        "level": 0.74
      },
      {
        "date": "nan",
        "level": 2.39
      },
      {
        "date": "2022-05-11",
        "level": 0.69
      },
      {
        "date": "2023-05-01",
        "level": 1.85
      },
      {
        "date": "nan",
        "level": 1.7
      },
      {
        "date": "nan",
        "level": 1.4
      },
      {
        "date": "2023-05-11",
        "level": 1.53
      },
      {
        "date": "2024-05-01",
        "level": 1.69
      }
    ]
  },
  {
    "name": "Heggadadevanakote",
    "district": "Mysore",
    "tehsil": "HEGGADADEVANKOTE",
    "block": "HEGGADADEVANKOTE",
    "village": "Heggadadevanakote",
    "latitude": 12.1,
    "longitude": 76.333333,
    "monitoringDate": "2024-01-05",
    "current": 11.0,
    "predicted": 11.81,
    "change": 0.81,
    "risk": "Moderate",
    "probabilities": {
      "no": 24.1,
      "low": 18.3,
      "moderate": 29.5,
      "high": 28.1
    },
    "history": [
      {
        "date": "nan",
        "level": 8.97
      },
      {
        "date": "nan",
        "level": 4.85
      },
      {
        "date": "2022-05-11",
        "level": 4.14
      },
      {
        "date": "2023-05-01",
        "level": 8.92
      },
      {
        "date": "nan",
        "level": 12.67
      },
      {
        "date": "nan",
        "level": 11.08
      },
      {
        "date": "2023-05-11",
        "level": 8.89
      },
      {
        "date": "2024-05-01",
        "level": 11.0
      }
    ]
  },
  {
    "name": "Heggadadevanakote-A",
    "district": "Mysore",
    "tehsil": "HEGGADADEVANKOTE",
    "block": "HEGGADADEVANKOTE",
    "village": "Heggadadevanakote-A",
    "latitude": 12.090556,
    "longitude": 76.329722,
    "monitoringDate": "2024-01-05",
    "current": 6.4,
    "predicted": 8.07,
    "change": 1.67,
    "risk": "No Depletion",
    "probabilities": {
      "no": 28.7,
      "low": 21.6,
      "moderate": 21.3,
      "high": 28.4
    },
    "history": [
      {
        "date": "nan",
        "level": 6.2
      },
      {
        "date": "2021-10-01",
        "level": 5.34
      },
      {
        "date": "nan",
        "level": 7.12
      },
      {
        "date": "nan",
        "level": 4.43
      },
      {
        "date": "nan",
        "level": 5.7
      },
      {
        "date": "nan",
        "level": 2.8
      },
      {
        "date": "2022-05-11",
        "level": 2.75
      },
      {
        "date": "2024-05-01",
        "level": 6.4
      }
    ]
  },
  {
    "name": "Heggadevanakote",
    "district": "Mysore",
    "tehsil": "HEGGADADEVANKOTE",
    "block": "HEGGADADEVANKOTE",
    "village": "Heggadevanakote",
    "latitude": 12.183333,
    "longitude": 76.275,
    "monitoringDate": "2023-01-05",
    "current": 5.05,
    "predicted": 6.36,
    "change": 1.31,
    "risk": "High",
    "probabilities": {
      "no": 21.6,
      "low": 27.1,
      "moderate": 23.7,
      "high": 27.6
    },
    "history": [
      {
        "date": "nan",
        "level": 2.98
      },
      {
        "date": "nan",
        "level": 18.83
      },
      {
        "date": "nan",
        "level": 5.7
      },
      {
        "date": "2019-01-05",
        "level": 7.3
      },
      {
        "date": "nan",
        "level": 2.31
      },
      {
        "date": "nan",
        "level": 3.99
      },
      {
        "date": "2020-10-01",
        "level": 2.86
      },
      {
        "date": "2023-05-01",
        "level": 5.05
      }
    ]
  },
  {
    "name": "Hejjodlu",
    "district": "Mysore",
    "tehsil": "HUNSUR",
    "block": "HUNSUR",
    "village": "Hejjodlu",
    "latitude": 12.379722,
    "longitude": 76.373611,
    "monitoringDate": "2024-01-05",
    "current": 14.1,
    "predicted": 15.73,
    "change": 1.63,
    "risk": "High",
    "probabilities": {
      "no": 30.5,
      "low": 8.8,
      "moderate": 16.0,
      "high": 44.7
    },
    "history": [
      {
        "date": "nan",
        "level": 12.95
      },
      {
        "date": "nan",
        "level": 12.8
      },
      {
        "date": "nan",
        "level": 8.15
      },
      {
        "date": "nan",
        "level": 5.87
      },
      {
        "date": "2022-05-11",
        "level": 5.4
      },
      {
        "date": "2023-05-01",
        "level": 13.7
      },
      {
        "date": "2023-05-11",
        "level": 4.64
      },
      {
        "date": "2024-05-01",
        "level": 14.1
      }
    ]
  },
  {
    "name": "Hosaramanahalli",
    "district": "Mysore",
    "tehsil": "KRISHNARAJANAGARA",
    "block": "KRISHNARAJANAGARA",
    "village": "Hosaramanahalli",
    "latitude": 12.366667,
    "longitude": 76.422222,
    "monitoringDate": "2022-08-25",
    "current": 2.3,
    "predicted": 5.16,
    "change": 2.86,
    "risk": "No Depletion",
    "probabilities": {
      "no": 43.0,
      "low": 16.0,
      "moderate": 8.6,
      "high": 32.4
    },
    "history": [
      {
        "date": "2020-10-01",
        "level": 14.2
      },
      {
        "date": "nan",
        "level": 8.3
      },
      {
        "date": "2021-10-01",
        "level": 20.3
      },
      {
        "date": "nan",
        "level": 19.75
      },
      {
        "date": "nan",
        "level": 10.51
      },
      {
        "date": "nan",
        "level": 11.2
      },
      {
        "date": "nan",
        "level": 2.85
      },
      {
        "date": "nan",
        "level": 2.3
      }
    ]
  },
  {
    "name": "Hosur1",
    "district": "Mysore",
    "tehsil": "KRISHNARAJANAGARA",
    "block": "KRISHNARAJANAGARA",
    "village": "Hosur",
    "latitude": 12.55,
    "longitude": 76.3,
    "monitoringDate": "2019-08-19",
    "current": 12.0,
    "predicted": 10.48,
    "change": -1.52,
    "risk": "No Depletion",
    "probabilities": {
      "no": 60.7,
      "low": 17.6,
      "moderate": 7.2,
      "high": 14.5
    },
    "history": [
      {
        "date": "2013-05-11",
        "level": 6.45
      },
      {
        "date": "2014-05-01",
        "level": 6.25
      },
      {
        "date": "nan",
        "level": 8.6
      },
      {
        "date": "nan",
        "level": 7.05
      },
      {
        "date": "2014-05-11",
        "level": 5.89
      },
      {
        "date": "2015-05-01",
        "level": 12.25
      },
      {
        "date": "nan",
        "level": 5.53
      },
      {
        "date": "nan",
        "level": 12.0
      }
    ]
  },
  {
    "name": "Huduguru",
    "district": "Mysore",
    "tehsil": "HUNSUR",
    "block": "HUNSUR",
    "village": "Huduguru",
    "latitude": 12.350556,
    "longitude": 76.291111,
    "monitoringDate": "2018-05-25",
    "current": 6.0,
    "predicted": 4.12,
    "change": -1.88,
    "risk": "No Depletion",
    "probabilities": {
      "no": 61.1,
      "low": 14.9,
      "moderate": 11.7,
      "high": 12.4
    },
    "history": [
      {
        "date": "2016-05-01",
        "level": 3.87
      },
      {
        "date": "nan",
        "level": 7.56
      },
      {
        "date": "2016-05-11",
        "level": 8.95
      },
      {
        "date": "2017-05-01",
        "level": 10.4
      },
      {
        "date": "nan",
        "level": 10.4
      },
      {
        "date": "nan",
        "level": 6.15
      },
      {
        "date": "2018-05-01",
        "level": 10.4
      },
      {
        "date": "nan",
        "level": 6.0
      }
    ]
  },
  {
    "name": "Hullahalli",
    "district": "Mysore",
    "tehsil": "NANJANGUD",
    "block": "NANJANGUD",
    "village": "Hullahalli",
    "latitude": 12.095,
    "longitude": 76.668889,
    "monitoringDate": "2024-01-05",
    "current": 9.33,
    "predicted": 7.47,
    "change": -1.86,
    "risk": "Moderate",
    "probabilities": {
      "no": 31.2,
      "low": 14.3,
      "moderate": 31.5,
      "high": 23.0
    },
    "history": [
      {
        "date": "nan",
        "level": 7.34
      },
      {
        "date": "nan",
        "level": 3.84
      },
      {
        "date": "2022-05-11",
        "level": 2.94
      },
      {
        "date": "2023-05-01",
        "level": 7.75
      },
      {
        "date": "nan",
        "level": 9.8
      },
      {
        "date": "nan",
        "level": 8.7
      },
      {
        "date": "2023-05-11",
        "level": 3.47
      },
      {
        "date": "2024-05-01",
        "level": 9.33
      }
    ]
  },
  {
    "name": "Hunsur A",
    "district": "Mysore",
    "tehsil": "HUNSUR",
    "block": "HUNSUR",
    "village": "Hunsur A",
    "latitude": 12.305556,
    "longitude": 76.275,
    "monitoringDate": "2024-01-05",
    "current": 3.5,
    "predicted": 5.52,
    "change": 2.02,
    "risk": "Low",
    "probabilities": {
      "no": 21.1,
      "low": 41.5,
      "moderate": 22.9,
      "high": 14.5
    },
    "history": [
      {
        "date": "nan",
        "level": 1.65
      },
      {
        "date": "nan",
        "level": 1.97
      },
      {
        "date": "2022-05-11",
        "level": 2.2
      },
      {
        "date": "2023-05-01",
        "level": 3.5
      },
      {
        "date": "nan",
        "level": 3.36
      },
      {
        "date": "nan",
        "level": 3.32
      },
      {
        "date": "2023-05-11",
        "level": 9.62
      },
      {
        "date": "2024-05-01",
        "level": 3.5
      }
    ]
  },
  {
    "name": "Hunsur1",
    "district": "Mysore",
    "tehsil": "HUNSUR",
    "block": "HUNSUR",
    "village": "Hunsur",
    "latitude": 12.308333,
    "longitude": 76.291667,
    "monitoringDate": "2024-01-05",
    "current": 12.0,
    "predicted": 16.48,
    "change": 4.48,
    "risk": "High",
    "probabilities": {
      "no": 32.1,
      "low": 11.9,
      "moderate": 18.8,
      "high": 37.2
    },
    "history": [
      {
        "date": "nan",
        "level": 10.77
      },
      {
        "date": "nan",
        "level": 6.61
      },
      {
        "date": "2022-05-11",
        "level": 5.54
      },
      {
        "date": "2023-05-01",
        "level": 21.2
      },
      {
        "date": "nan",
        "level": 25.22
      },
      {
        "date": "nan",
        "level": 11.42
      },
      {
        "date": "2023-05-11",
        "level": 24.62
      },
      {
        "date": "2024-05-01",
        "level": 12.0
      }
    ]
  },
  {
    "name": "Hunsur1_1",
    "district": "Mysore",
    "tehsil": "-",
    "block": "-",
    "village": "-",
    "latitude": 12.3083,
    "longitude": 76.2842,
    "monitoringDate": "2024-01-05",
    "current": 27.2,
    "predicted": 19.98,
    "change": -7.22,
    "risk": "No Depletion",
    "probabilities": {
      "no": 45.6,
      "low": 11.1,
      "moderate": 18.7,
      "high": 24.6
    },
    "history": [
      {
        "date": "nan",
        "level": 25.66
      },
      {
        "date": "2024-05-01",
        "level": 27.2
      }
    ]
  },
  {
    "name": "Hunugunahalli",
    "district": "Mysore",
    "tehsil": "TIRUMAKUDAL-NARSIPUR",
    "block": "TIRUMAKUDAL-NARSIPUR",
    "village": "Hunugunahalli",
    "latitude": 12.254722,
    "longitude": 76.910556,
    "monitoringDate": "2024-01-05",
    "current": 2.26,
    "predicted": 6.54,
    "change": 4.28,
    "risk": "High",
    "probabilities": {
      "no": 15.0,
      "low": 18.8,
      "moderate": 13.6,
      "high": 52.7
    },
    "history": [
      {
        "date": "nan",
        "level": 0.3
      },
      {
        "date": "nan",
        "level": 0.7
      },
      {
        "date": "2022-05-11",
        "level": 0.6
      },
      {
        "date": "2023-05-01",
        "level": 1.9
      },
      {
        "date": "nan",
        "level": 4.35
      },
      {
        "date": "nan",
        "level": 4.88
      },
      {
        "date": "2023-05-11",
        "level": 2.36
      },
      {
        "date": "2024-05-01",
        "level": 2.26
      }
    ]
  },
  {
    "name": "Ibjala",
    "district": "Mysore",
    "tehsil": "NANJANGUD",
    "block": "NANJANGUD",
    "village": "Ibjala",
    "latitude": 12.112778,
    "longitude": 76.446944,
    "monitoringDate": "2024-01-05",
    "current": 5.13,
    "predicted": 9.42,
    "change": 4.29,
    "risk": "High",
    "probabilities": {
      "no": 28.5,
      "low": 16.2,
      "moderate": 24.3,
      "high": 31.0
    },
    "history": [
      {
        "date": "nan",
        "level": 3.1
      },
      {
        "date": "nan",
        "level": 2.55
      },
      {
        "date": "2022-05-11",
        "level": 2.6
      },
      {
        "date": "2023-05-01",
        "level": 4.8
      },
      {
        "date": "nan",
        "level": 5.78
      },
      {
        "date": "nan",
        "level": 4.0
      },
      {
        "date": "2023-05-11",
        "level": 9.62
      },
      {
        "date": "2024-05-01",
        "level": 5.13
      }
    ]
  },
  {
    "name": "Jayapura(CHATNAHALLI)",
    "district": "Mysore",
    "tehsil": "MYSORE",
    "block": "MYSORE",
    "village": "JAYAPUR(CHATNAHALLI)",
    "latitude": 12.204167,
    "longitude": 76.552778,
    "monitoringDate": "2013-05-15",
    "current": 3.53,
    "predicted": 7.44,
    "change": 3.91,
    "risk": "No Depletion",
    "probabilities": {
      "no": 47.2,
      "low": 14.9,
      "moderate": 11.4,
      "high": 26.6
    },
    "history": [
      {
        "date": "2007-05-01",
        "level": 12.63
      },
      {
        "date": "nan",
        "level": 12.63
      },
      {
        "date": "nan",
        "level": 12.63
      },
      {
        "date": "2008-05-11",
        "level": 12.63
      },
      {
        "date": "nan",
        "level": 12.63
      },
      {
        "date": "2011-05-11",
        "level": 12.63
      },
      {
        "date": "2013-05-01",
        "level": 12.63
      },
      {
        "date": "nan",
        "level": 3.53
      }
    ]
  },
  {
    "name": "Jayapura1",
    "district": "Mysore",
    "tehsil": "MYSORE",
    "block": "MYSORE",
    "village": "Jayapura",
    "latitude": 12.225,
    "longitude": 76.608333,
    "monitoringDate": "2006-11-05",
    "current": 17.77,
    "predicted": 16.94,
    "change": -0.83,
    "risk": "No Depletion",
    "probabilities": {
      "no": 28.7,
      "low": 25.1,
      "moderate": 20.8,
      "high": 25.4
    },
    "history": [
      {
        "date": "nan",
        "level": 10.04
      },
      {
        "date": "2004-05-11",
        "level": 4.5
      },
      {
        "date": "nan",
        "level": 10.51
      },
      {
        "date": "nan",
        "level": 9.91
      },
      {
        "date": "2005-05-11",
        "level": 17.77
      },
      {
        "date": "2006-05-01",
        "level": 17.77
      },
      {
        "date": "nan",
        "level": 17.77
      },
      {
        "date": "2006-05-11",
        "level": 17.77
      }
    ]
  },
  {
    "name": "Kahalli",
    "district": "Mysore",
    "tehsil": "NANJANGUD",
    "block": "NANJANGUD",
    "village": "Kahalli",
    "latitude": 12.163611,
    "longitude": 76.841111,
    "monitoringDate": "2024-01-05",
    "current": 11.63,
    "predicted": 13.43,
    "change": 1.8,
    "risk": "No Depletion",
    "probabilities": {
      "no": 31.5,
      "low": 12.8,
      "moderate": 25.6,
      "high": 30.1
    },
    "history": [
      {
        "date": "nan",
        "level": 9.6
      },
      {
        "date": "nan",
        "level": 5.9
      },
      {
        "date": "nan",
        "level": 5.3
      },
      {
        "date": "2022-05-11",
        "level": 4.82
      },
      {
        "date": "2023-05-01",
        "level": 10.2
      },
      {
        "date": "nan",
        "level": 15.4
      },
      {
        "date": "nan",
        "level": 14.78
      },
      {
        "date": "2024-05-01",
        "level": 11.63
      }
    ]
  },
  {
    "name": "Kalasthavadi",
    "district": "Mysore",
    "tehsil": "MYSORE",
    "block": "MYSORE",
    "village": "Kalasthavadi",
    "latitude": 12.361111,
    "longitude": 76.661111,
    "monitoringDate": "2022-08-25",
    "current": 2.5,
    "predicted": 2.91,
    "change": 0.41,
    "risk": "No Depletion",
    "probabilities": {
      "no": 61.7,
      "low": 25.0,
      "moderate": 8.5,
      "high": 4.9
    },
    "history": [
      {
        "date": "2020-10-01",
        "level": 4.71
      },
      {
        "date": "nan",
        "level": 1.45
      },
      {
        "date": "2021-10-01",
        "level": 2.22
      },
      {
        "date": "nan",
        "level": 5.22
      },
      {
        "date": "nan",
        "level": 2.11
      },
      {
        "date": "nan",
        "level": 3.4
      },
      {
        "date": "nan",
        "level": 2.21
      },
      {
        "date": "nan",
        "level": 2.5
      }
    ]
  },
  {
    "name": "Kalayanapura",
    "district": "Mysore",
    "tehsil": "KRISHNARAJANAGARA",
    "block": "KRISHNARAJANAGARA",
    "village": "Kalayanapura",
    "latitude": 12.325,
    "longitude": 76.283333,
    "monitoringDate": "2023-05-26",
    "current": 3.2,
    "predicted": 5.3,
    "change": 2.1,
    "risk": "No Depletion",
    "probabilities": {
      "no": 42.1,
      "low": 25.3,
      "moderate": 18.2,
      "high": 14.4
    },
    "history": [
      {
        "date": "nan",
        "level": 16.5
      },
      {
        "date": "nan",
        "level": 11.93
      },
      {
        "date": "2016-05-11",
        "level": 11.0
      },
      {
        "date": "2017-05-01",
        "level": 19.2
      },
      {
        "date": "nan",
        "level": 12.0
      },
      {
        "date": "nan",
        "level": 7.05
      },
      {
        "date": "2020-10-01",
        "level": 3.53
      },
      {
        "date": "nan",
        "level": 3.2
      }
    ]
  },
  {
    "name": "Kamalapura",
    "district": "Mysore",
    "tehsil": "PIRIYAPATNA",
    "block": "PIRIYAPATNA",
    "village": "Kampalapura",
    "latitude": 12.333333,
    "longitude": 76.108333,
    "monitoringDate": "2023-08-25",
    "current": 2.6,
    "predicted": 2.77,
    "change": 0.17,
    "risk": "Low",
    "probabilities": {
      "no": 42.3,
      "low": 48.7,
      "moderate": 4.7,
      "high": 4.2
    },
    "history": [
      {
        "date": "nan",
        "level": 2.02
      },
      {
        "date": "nan",
        "level": 3.05
      },
      {
        "date": "nan",
        "level": 1.35
      },
      {
        "date": "nan",
        "level": 2.2
      },
      {
        "date": "2022-05-11",
        "level": 2.18
      },
      {
        "date": "2023-05-01",
        "level": 3.4
      },
      {
        "date": "nan",
        "level": 3.58
      },
      {
        "date": "nan",
        "level": 2.6
      }
    ]
  },
  {
    "name": "Kannenuru",
    "district": "Mysore",
    "tehsil": "NANJANGUD",
    "block": "NANJANGUD",
    "village": "Kannenuru",
    "latitude": 12.097222,
    "longitude": 76.513889,
    "monitoringDate": "2024-01-05",
    "current": 8.7,
    "predicted": 7.75,
    "change": -0.95,
    "risk": "High",
    "probabilities": {
      "no": 30.3,
      "low": 13.2,
      "moderate": 21.0,
      "high": 35.5
    },
    "history": [
      {
        "date": "nan",
        "level": 4.3
      },
      {
        "date": "nan",
        "level": 4.1
      },
      {
        "date": "2022-05-11",
        "level": 4.2
      },
      {
        "date": "2023-05-01",
        "level": 8.85
      },
      {
        "date": "nan",
        "level": 4.9
      },
      {
        "date": "nan",
        "level": 8.5
      },
      {
        "date": "2023-05-11",
        "level": 2.09
      },
      {
        "date": "2024-05-01",
        "level": 8.7
      }
    ]
  },
  {
    "name": "Karimuddanahalli",
    "district": "Mysore",
    "tehsil": "HUNSUR",
    "block": "HUNSUR",
    "village": "Karimuddanahalli",
    "latitude": 12.184167,
    "longitude": 76.366667,
    "monitoringDate": "2024-01-05",
    "current": 17.7,
    "predicted": 19.53,
    "change": 1.83,
    "risk": "High",
    "probabilities": {
      "no": 26.9,
      "low": 9.8,
      "moderate": 24.1,
      "high": 39.2
    },
    "history": [
      {
        "date": "nan",
        "level": 17.19
      },
      {
        "date": "nan",
        "level": 14.3
      },
      {
        "date": "nan",
        "level": 10.4
      },
      {
        "date": "2022-05-11",
        "level": 9.68
      },
      {
        "date": "2023-05-01",
        "level": 15.41
      },
      {
        "date": "nan",
        "level": 16.72
      },
      {
        "date": "2023-05-11",
        "level": 15.17
      },
      {
        "date": "2024-05-01",
        "level": 17.7
      }
    ]
  },
  {
    "name": "Karimuddanahalli1",
    "district": "Mysore",
    "tehsil": "HEGGADADEVANKOTE",
    "block": "HEGGADADEVANKOTE",
    "village": "Karimuddanahalli",
    "latitude": 12.091667,
    "longitude": 76.375,
    "monitoringDate": "2002-01-05",
    "current": 3.28,
    "predicted": 7.22,
    "change": 3.94,
    "risk": "High",
    "probabilities": {
      "no": 16.6,
      "low": 16.6,
      "moderate": 22.4,
      "high": 44.3
    },
    "history": [
      {
        "date": "2000-05-01",
        "level": 3.93
      },
      {
        "date": "nan",
        "level": 7.97
      },
      {
        "date": "nan",
        "level": 3.39
      },
      {
        "date": "2001-05-01",
        "level": 9.57
      },
      {
        "date": "nan",
        "level": 7.11
      },
      {
        "date": "nan",
        "level": 1.37
      },
      {
        "date": "2001-05-11",
        "level": 0.65
      },
      {
        "date": "2002-05-01",
        "level": 3.28
      }
    ]
  },
  {
    "name": "Karimuddanahalli_1",
    "district": "Mysore",
    "tehsil": "-",
    "block": "-",
    "village": "-",
    "latitude": 12.1842,
    "longitude": 76.3667,
    "monitoringDate": "2023-08-25",
    "current": 17.42,
    "predicted": 14.75,
    "change": -2.67,
    "risk": "No Depletion",
    "probabilities": {
      "no": 65.8,
      "low": 10.6,
      "moderate": 11.8,
      "high": 11.8
    },
    "history": [
      {
        "date": "nan",
        "level": 17.42
      }
    ]
  },
  {
    "name": "Karnakuppe",
    "district": "Mysore",
    "tehsil": "HUNSUR",
    "block": "HUNSUR",
    "village": "Karnakuppe",
    "latitude": 12.2375,
    "longitude": 76.191667,
    "monitoringDate": "2013-01-05",
    "current": 14.41,
    "predicted": 9.84,
    "change": -4.57,
    "risk": "No Depletion",
    "probabilities": {
      "no": 36.8,
      "low": 12.4,
      "moderate": 16.2,
      "high": 34.7
    },
    "history": [
      {
        "date": "nan",
        "level": 0.94
      },
      {
        "date": "2006-05-11",
        "level": 0.95
      },
      {
        "date": "2007-05-01",
        "level": 2.49
      },
      {
        "date": "nan",
        "level": 14.4
      },
      {
        "date": "nan",
        "level": 0.74
      },
      {
        "date": "2007-05-11",
        "level": 0.75
      },
      {
        "date": "nan",
        "level": 4.95
      },
      {
        "date": "2013-05-01",
        "level": 14.41
      }
    ]
  },
  {
    "name": "Kellanapura",
    "district": "Mysore",
    "tehsil": "MYSORE",
    "block": "MYSORE",
    "village": "Kellanapura",
    "latitude": 12.254444,
    "longitude": 76.816944,
    "monitoringDate": "2024-01-05",
    "current": 5.1,
    "predicted": 9.05,
    "change": 3.95,
    "risk": "Moderate",
    "probabilities": {
      "no": 24.8,
      "low": 25.6,
      "moderate": 26.4,
      "high": 23.1
    },
    "history": [
      {
        "date": "2017-05-11",
        "level": 3.57
      },
      {
        "date": "2018-05-01",
        "level": 7.67
      },
      {
        "date": "nan",
        "level": 8.67
      },
      {
        "date": "nan",
        "level": 1.57
      },
      {
        "date": "nan",
        "level": 1.97
      },
      {
        "date": "nan",
        "level": 1.02
      },
      {
        "date": "2022-05-11",
        "level": 0.92
      },
      {
        "date": "2024-05-01",
        "level": 5.1
      }
    ]
  },
  {
    "name": "Kethupura",
    "district": "Mysore",
    "tehsil": "MYSORE",
    "block": "MYSORE",
    "village": "Kethupura",
    "latitude": 12.3,
    "longitude": 76.888056,
    "monitoringDate": "2024-01-05",
    "current": 2.92,
    "predicted": 3.3,
    "change": 0.38,
    "risk": "Moderate",
    "probabilities": {
      "no": 24.4,
      "low": 28.6,
      "moderate": 33.1,
      "high": 13.9
    },
    "history": [
      {
        "date": "nan",
        "level": 0.9
      },
      {
        "date": "nan",
        "level": 1.25
      },
      {
        "date": "2022-05-11",
        "level": 1.25
      },
      {
        "date": "2023-05-01",
        "level": 3.05
      },
      {
        "date": "nan",
        "level": 2.95
      },
      {
        "date": "nan",
        "level": 2.43
      },
      {
        "date": "2023-05-11",
        "level": 2.42
      },
      {
        "date": "2024-05-01",
        "level": 2.92
      }
    ]
  },
  {
    "name": "Kittur",
    "district": "Mysore",
    "tehsil": "PIRIYAPATNA",
    "block": "PIRIYAPATNA",
    "village": "Kithoor",
    "latitude": 12.477778,
    "longitude": 76.1,
    "monitoringDate": "2024-01-05",
    "current": 5.6,
    "predicted": 10.31,
    "change": 4.71,
    "risk": "Moderate",
    "probabilities": {
      "no": 18.0,
      "low": 20.9,
      "moderate": 44.8,
      "high": 16.3
    },
    "history": [
      {
        "date": "nan",
        "level": 4.41
      },
      {
        "date": "nan",
        "level": 1.8
      },
      {
        "date": "nan",
        "level": 2.2
      },
      {
        "date": "2022-05-11",
        "level": 1.2
      },
      {
        "date": "2023-05-01",
        "level": 6.1
      },
      {
        "date": "nan",
        "level": 7.73
      },
      {
        "date": "nan",
        "level": 5.95
      },
      {
        "date": "2024-05-01",
        "level": 5.6
      }
    ]
  },
  {
    "name": "Koimuthur Colony",
    "district": "Mysore",
    "tehsil": "HUNSUR",
    "block": "HUNSUR",
    "village": "Koimuthur Colony",
    "latitude": 12.250278,
    "longitude": 76.331389,
    "monitoringDate": "2024-01-05",
    "current": 8.9,
    "predicted": 10.92,
    "change": 2.02,
    "risk": "High",
    "probabilities": {
      "no": 22.1,
      "low": 11.8,
      "moderate": 11.5,
      "high": 54.6
    },
    "history": [
      {
        "date": "nan",
        "level": 3.47
      },
      {
        "date": "nan",
        "level": 3.25
      },
      {
        "date": "nan",
        "level": 2.85
      },
      {
        "date": "nan",
        "level": 1.5
      },
      {
        "date": "2022-05-11",
        "level": 1.65
      },
      {
        "date": "2023-05-01",
        "level": 3.5
      },
      {
        "date": "2023-05-11",
        "level": 7.93
      },
      {
        "date": "2024-05-01",
        "level": 8.9
      }
    ]
  },
  {
    "name": "Konasuru",
    "district": "Mysore",
    "tehsil": "PIRIYAPATNA",
    "block": "PIRIYAPATNA",
    "village": "Konasuru",
    "latitude": 12.448056,
    "longitude": 76.071111,
    "monitoringDate": "2024-01-05",
    "current": 2.26,
    "predicted": 6.79,
    "change": 4.53,
    "risk": "Low",
    "probabilities": {
      "no": 19.8,
      "low": 33.1,
      "moderate": 24.5,
      "high": 22.6
    },
    "history": [
      {
        "date": "nan",
        "level": 1.15
      },
      {
        "date": "nan",
        "level": 1.25
      },
      {
        "date": "2022-05-11",
        "level": 1.24
      },
      {
        "date": "2023-05-01",
        "level": 2.25
      },
      {
        "date": "nan",
        "level": 2.21
      },
      {
        "date": "nan",
        "level": 1.95
      },
      {
        "date": "2023-05-11",
        "level": 1.9
      },
      {
        "date": "2024-05-01",
        "level": 2.26
      }
    ]
  },
  {
    "name": "Kothanahalli",
    "district": "Mysore",
    "tehsil": "NANJANGUD",
    "block": "NANJANGUD",
    "village": "Kothanahalli",
    "latitude": 11.925,
    "longitude": 76.568056,
    "monitoringDate": "2024-01-05",
    "current": 8.85,
    "predicted": 9.77,
    "change": 0.92,
    "risk": "No Depletion",
    "probabilities": {
      "no": 31.4,
      "low": 15.8,
      "moderate": 30.1,
      "high": 22.7
    },
    "history": [
      {
        "date": "nan",
        "level": 6.36
      },
      {
        "date": "nan",
        "level": 4.64
      },
      {
        "date": "2022-05-11",
        "level": 4.86
      },
      {
        "date": "2023-05-01",
        "level": 6.35
      },
      {
        "date": "nan",
        "level": 7.0
      },
      {
        "date": "nan",
        "level": 6.98
      },
      {
        "date": "2023-05-11",
        "level": 4.71
      },
      {
        "date": "2024-05-01",
        "level": 8.85
      }
    ]
  },
  {
    "name": "Krishnarajanagara",
    "district": "Mysore",
    "tehsil": "KRISHNARAJANAGARA",
    "block": "KRISHNARAJANAGARA",
    "village": "Krishnarajanagara",
    "latitude": 12.466667,
    "longitude": 76.383333,
    "monitoringDate": "2024-01-05",
    "current": 11.03,
    "predicted": 12.49,
    "change": 1.46,
    "risk": "Moderate",
    "probabilities": {
      "no": 24.2,
      "low": 16.8,
      "moderate": 33.7,
      "high": 25.4
    },
    "history": [
      {
        "date": "nan",
        "level": 1.96
      },
      {
        "date": "nan",
        "level": 8.75
      },
      {
        "date": "nan",
        "level": 2.4
      },
      {
        "date": "2022-05-11",
        "level": 6.95
      },
      {
        "date": "2023-05-01",
        "level": 10.61
      },
      {
        "date": "nan",
        "level": 10.36
      },
      {
        "date": "2023-05-11",
        "level": 9.04
      },
      {
        "date": "2024-05-01",
        "level": 11.03
      }
    ]
  },
  {
    "name": "Krishnarajanagara1",
    "district": "Mysore",
    "tehsil": "HUNSUR",
    "block": "HUNSUR",
    "village": "Krishnarajanagara",
    "latitude": 12.325,
    "longitude": 76.283333,
    "monitoringDate": "2024-01-05",
    "current": 4.47,
    "predicted": 5.75,
    "change": 1.28,
    "risk": "Low",
    "probabilities": {
      "no": 24.4,
      "low": 41.1,
      "moderate": 23.3,
      "high": 11.3
    },
    "history": [
      {
        "date": "nan",
        "level": 3.02
      },
      {
        "date": "nan",
        "level": 1.47
      },
      {
        "date": "nan",
        "level": 2.27
      },
      {
        "date": "2022-05-11",
        "level": 2.12
      },
      {
        "date": "2023-05-01",
        "level": 4.35
      },
      {
        "date": "nan",
        "level": 3.78
      },
      {
        "date": "nan",
        "level": 4.02
      },
      {
        "date": "2024-05-01",
        "level": 4.47
      }
    ]
  },
  {
    "name": "Kundanahalli",
    "district": "Mysore",
    "tehsil": "PIRIYAPATNA",
    "block": "PIRIYAPATNA",
    "village": "Kundanahalli",
    "latitude": 12.375,
    "longitude": 76.038889,
    "monitoringDate": "2021-11-30",
    "current": 1.86,
    "predicted": 5.09,
    "change": 3.23,
    "risk": "High",
    "probabilities": {
      "no": 15.9,
      "low": 21.7,
      "moderate": 29.0,
      "high": 33.5
    },
    "history": [
      {
        "date": "nan",
        "level": 11.2
      },
      {
        "date": "nan",
        "level": 9.7
      },
      {
        "date": "2017-05-11",
        "level": 11.2
      },
      {
        "date": "2018-05-01",
        "level": 11.2
      },
      {
        "date": "nan",
        "level": 11.2
      },
      {
        "date": "nan",
        "level": 11.2
      },
      {
        "date": "nan",
        "level": 11.2
      },
      {
        "date": "nan",
        "level": 1.86
      }
    ]
  },
  {
    "name": "Mayagowdanahalli",
    "district": "Mysore",
    "tehsil": "KRISHNARAJANAGARA",
    "block": "KRISHNARAJANAGARA",
    "village": "Mayagowdanahalli",
    "latitude": 12.500556,
    "longitude": 76.242222,
    "monitoringDate": "2024-01-05",
    "current": 10.1,
    "predicted": 10.16,
    "change": 0.06,
    "risk": "Moderate",
    "probabilities": {
      "no": 28.9,
      "low": 19.5,
      "moderate": 32.1,
      "high": 19.5
    },
    "history": [
      {
        "date": "nan",
        "level": 8.02
      },
      {
        "date": "nan",
        "level": 4.75
      },
      {
        "date": "nan",
        "level": 7.75
      },
      {
        "date": "2022-05-11",
        "level": 6.7
      },
      {
        "date": "2023-05-01",
        "level": 7.73
      },
      {
        "date": "nan",
        "level": 10.4
      },
      {
        "date": "2023-05-11",
        "level": 8.03
      },
      {
        "date": "2024-05-01",
        "level": 10.1
      }
    ]
  },
  {
    "name": "Motha",
    "district": "Mysore",
    "tehsil": "NANJANGUD",
    "block": "NANJANGUD",
    "village": "Motha",
    "latitude": 12.094444,
    "longitude": 76.477778,
    "monitoringDate": "2024-01-05",
    "current": 2.23,
    "predicted": 4.55,
    "change": 2.32,
    "risk": "High",
    "probabilities": {
      "no": 25.2,
      "low": 24.0,
      "moderate": 22.0,
      "high": 28.8
    },
    "history": [
      {
        "date": "nan",
        "level": 0.9
      },
      {
        "date": "nan",
        "level": 1.28
      },
      {
        "date": "2022-05-11",
        "level": 0.95
      },
      {
        "date": "2023-05-01",
        "level": 2.45
      },
      {
        "date": "nan",
        "level": 1.86
      },
      {
        "date": "nan",
        "level": 2.07
      },
      {
        "date": "2023-05-11",
        "level": 5.33
      },
      {
        "date": "2024-05-01",
        "level": 2.23
      }
    ]
  },
  {
    "name": "Muguru",
    "district": "Mysore",
    "tehsil": "TIRUMAKUDAL-NARSIPUR",
    "block": "TIRUMAKUDAL-NARSIPUR",
    "village": "Muguru",
    "latitude": 12.125,
    "longitude": 76.95,
    "monitoringDate": "2019-08-19",
    "current": 5.3,
    "predicted": 6.67,
    "change": 1.37,
    "risk": "No Depletion",
    "probabilities": {
      "no": 64.2,
      "low": 13.7,
      "moderate": 11.2,
      "high": 10.9
    },
    "history": [
      {
        "date": "nan",
        "level": 9.25
      },
      {
        "date": "2014-05-11",
        "level": 2.0
      },
      {
        "date": "2015-05-01",
        "level": 5.57
      },
      {
        "date": "nan",
        "level": 6.43
      },
      {
        "date": "2017-05-01",
        "level": 10.2
      },
      {
        "date": "nan",
        "level": 14.75
      },
      {
        "date": "2017-05-11",
        "level": 11.05
      },
      {
        "date": "nan",
        "level": 5.3
      }
    ]
  },
  {
    "name": "Muguru1",
    "district": "Mysore",
    "tehsil": "PIRIYAPATNA",
    "block": "PIRIYAPATNA",
    "village": "Muguru",
    "latitude": 12.336111,
    "longitude": 76.161111,
    "monitoringDate": "2024-01-05",
    "current": 11.1,
    "predicted": 10.94,
    "change": -0.16,
    "risk": "High",
    "probabilities": {
      "no": 24.0,
      "low": 18.8,
      "moderate": 19.6,
      "high": 37.7
    },
    "history": [
      {
        "date": "nan",
        "level": 7.75
      },
      {
        "date": "nan",
        "level": 9.2
      },
      {
        "date": "nan",
        "level": 5.6
      },
      {
        "date": "2022-05-11",
        "level": 4.4
      },
      {
        "date": "2023-05-01",
        "level": 8.45
      },
      {
        "date": "nan",
        "level": 12.1
      },
      {
        "date": "2023-05-11",
        "level": 2.96
      },
      {
        "date": "2024-05-01",
        "level": 11.1
      }
    ]
  },
  {
    "name": "Mullur",
    "district": "Mysore",
    "tehsil": "HEGGADADEVANKOTE",
    "block": "HEGGADADEVANKOTE",
    "village": "Mullur",
    "latitude": 11.983889,
    "longitude": 76.466667,
    "monitoringDate": "2024-01-05",
    "current": 16.4,
    "predicted": 16.95,
    "change": 0.55,
    "risk": "Moderate",
    "probabilities": {
      "no": 24.0,
      "low": 8.8,
      "moderate": 34.1,
      "high": 33.2
    },
    "history": [
      {
        "date": "nan",
        "level": 14.35
      },
      {
        "date": "nan",
        "level": 7.19
      },
      {
        "date": "2022-05-11",
        "level": 8.14
      },
      {
        "date": "2023-05-01",
        "level": 14.13
      },
      {
        "date": "nan",
        "level": 16.56
      },
      {
        "date": "nan",
        "level": 15.42
      },
      {
        "date": "2023-05-11",
        "level": 10.41
      },
      {
        "date": "2024-05-01",
        "level": 16.4
      }
    ]
  },
  {
    "name": "Mulluru",
    "district": "Mysore",
    "tehsil": "HEGGADADEVANKOTE",
    "block": "HEGGADADEVANKOTE",
    "village": "Mullur",
    "latitude": 11.983333,
    "longitude": 76.479167,
    "monitoringDate": "2024-01-05",
    "current": 13.0,
    "predicted": 14.07,
    "change": 1.07,
    "risk": "Moderate",
    "probabilities": {
      "no": 21.6,
      "low": 17.1,
      "moderate": 37.9,
      "high": 23.4
    },
    "history": [
      {
        "date": "nan",
        "level": 11.77
      },
      {
        "date": "nan",
        "level": 12.97
      },
      {
        "date": "nan",
        "level": 5.52
      },
      {
        "date": "2022-05-11",
        "level": 6.22
      },
      {
        "date": "2023-05-01",
        "level": 10.9
      },
      {
        "date": "nan",
        "level": 13.58
      },
      {
        "date": "nan",
        "level": 12.0
      },
      {
        "date": "2024-05-01",
        "level": 13.0
      }
    ]
  },
  {
    "name": "Mysore",
    "district": "Mysore",
    "tehsil": "MYSORE",
    "block": "MYSORE",
    "village": "Mysore",
    "latitude": 12.3,
    "longitude": 76.641667,
    "monitoringDate": "2024-01-05",
    "current": 12.8,
    "predicted": 12.36,
    "change": -0.44,
    "risk": "No Depletion",
    "probabilities": {
      "no": 34.7,
      "low": 25.1,
      "moderate": 27.9,
      "high": 12.3
    },
    "history": [
      {
        "date": "nan",
        "level": 9.81
      },
      {
        "date": "nan",
        "level": 8.96
      },
      {
        "date": "2022-05-11",
        "level": 8.73
      },
      {
        "date": "2023-05-01",
        "level": 11.18
      },
      {
        "date": "nan",
        "level": 11.85
      },
      {
        "date": "nan",
        "level": 12.05
      },
      {
        "date": "2023-05-11",
        "level": 11.43
      },
      {
        "date": "2024-05-01",
        "level": 12.8
      }
    ]
  },
  {
    "name": "Mysore1",
    "district": "Mysore",
    "tehsil": "MYSORE",
    "block": "MYSORE",
    "village": "Mysore",
    "latitude": 12.358333,
    "longitude": 76.5375,
    "monitoringDate": "2024-01-05",
    "current": 15.2,
    "predicted": 14.13,
    "change": -1.07,
    "risk": "No Depletion",
    "probabilities": {
      "no": 30.6,
      "low": 29.5,
      "moderate": 20.6,
      "high": 19.3
    },
    "history": [
      {
        "date": "nan",
        "level": 8.8
      },
      {
        "date": "nan",
        "level": 8.45
      },
      {
        "date": "nan",
        "level": 8.3
      },
      {
        "date": "2022-05-11",
        "level": 9.25
      },
      {
        "date": "nan",
        "level": 13.2
      },
      {
        "date": "nan",
        "level": 10.5
      },
      {
        "date": "2023-05-11",
        "level": 13.57
      },
      {
        "date": "2024-05-01",
        "level": 15.2
      }
    ]
  },
  {
    "name": "Mysore_1",
    "district": "Mysore",
    "tehsil": "MYSORE",
    "block": "-",
    "village": "-",
    "latitude": 12.3,
    "longitude": 76.63,
    "monitoringDate": "2023-01-05",
    "current": 13.45,
    "predicted": 11.14,
    "change": -2.31,
    "risk": "No Depletion",
    "probabilities": {
      "no": 35.0,
      "low": 25.4,
      "moderate": 23.0,
      "high": 16.6
    },
    "history": [
      {
        "date": "2023-05-01",
        "level": 13.45
      }
    ]
  },
  {
    "name": "Nanjanayakanahalli",
    "district": "Mysore",
    "tehsil": "HEGGADADEVANKOTE",
    "block": "HEGGADADEVANKOTE",
    "village": "Nanjanayakanahalli",
    "latitude": 12.1,
    "longitude": 76.333333,
    "monitoringDate": "2024-01-05",
    "current": 9.82,
    "predicted": 9.16,
    "change": -0.66,
    "risk": "High",
    "probabilities": {
      "no": 31.1,
      "low": 14.3,
      "moderate": 22.2,
      "high": 32.4
    },
    "history": [
      {
        "date": "nan",
        "level": 2.86
      },
      {
        "date": "nan",
        "level": 1.96
      },
      {
        "date": "nan",
        "level": 2.11
      },
      {
        "date": "2022-05-11",
        "level": 2.51
      },
      {
        "date": "2023-05-01",
        "level": 3.85
      },
      {
        "date": "nan",
        "level": 7.05
      },
      {
        "date": "nan",
        "level": 7.35
      },
      {
        "date": "2024-05-01",
        "level": 9.82
      }
    ]
  },
  {
    "name": "Nanjangud",
    "district": "Mysore",
    "tehsil": "NANJANGUD",
    "block": "NANJANGUD",
    "village": "Nanjangud",
    "latitude": 12.066667,
    "longitude": 76.627778,
    "monitoringDate": "2013-01-05",
    "current": 9.32,
    "predicted": 9.43,
    "change": 0.11,
    "risk": "No Depletion",
    "probabilities": {
      "no": 41.7,
      "low": 14.5,
      "moderate": 22.3,
      "high": 21.5
    },
    "history": [
      {
        "date": "2009-05-11",
        "level": 5.82
      },
      {
        "date": "2010-05-01",
        "level": 5.51
      },
      {
        "date": "nan",
        "level": 2.74
      },
      {
        "date": "nan",
        "level": 3.3
      },
      {
        "date": "2011-05-11",
        "level": 2.92
      },
      {
        "date": "2012-05-01",
        "level": 5.3
      },
      {
        "date": "2012-05-11",
        "level": 2.7
      },
      {
        "date": "2013-05-01",
        "level": 9.32
      }
    ]
  },
  {
    "name": "P Basavanahalli",
    "district": "Mysore",
    "tehsil": "PIRIYAPATNA",
    "block": "PIRIYAPATNA",
    "village": "P Basavanahalli",
    "latitude": 12.426667,
    "longitude": 76.061389,
    "monitoringDate": "2024-01-05",
    "current": 22.1,
    "predicted": 22.24,
    "change": 0.14,
    "risk": "High",
    "probabilities": {
      "no": 27.3,
      "low": 12.1,
      "moderate": 18.5,
      "high": 42.1
    },
    "history": [
      {
        "date": "2016-05-01",
        "level": 23.76
      },
      {
        "date": "nan",
        "level": 22.5
      },
      {
        "date": "2017-05-01",
        "level": 23.27
      },
      {
        "date": "2019-05-01",
        "level": 23.0
      },
      {
        "date": "nan",
        "level": 21.7
      },
      {
        "date": "nan",
        "level": 21.53
      },
      {
        "date": "2023-05-11",
        "level": 4.1
      },
      {
        "date": "2024-05-01",
        "level": 22.1
      }
    ]
  },
  {
    "name": "Palya",
    "district": "Mysore",
    "tehsil": "NANJANGUD",
    "block": "NANJANGUD",
    "village": "Palya",
    "latitude": 12.095,
    "longitude": 76.668889,
    "monitoringDate": "2024-01-05",
    "current": 4.6,
    "predicted": 7.69,
    "change": 3.09,
    "risk": "High",
    "probabilities": {
      "no": 24.7,
      "low": 13.1,
      "moderate": 23.6,
      "high": 38.6
    },
    "history": [
      {
        "date": "nan",
        "level": 2.64
      },
      {
        "date": "nan",
        "level": 0.83
      },
      {
        "date": "2022-05-11",
        "level": 0.75
      },
      {
        "date": "2023-05-01",
        "level": 5.36
      },
      {
        "date": "nan",
        "level": 7.85
      },
      {
        "date": "nan",
        "level": 6.5
      },
      {
        "date": "2023-05-11",
        "level": 1.78
      },
      {
        "date": "2024-05-01",
        "level": 4.6
      }
    ]
  },
  {
    "name": "Piriyapatna",
    "district": "Mysore",
    "tehsil": "PIRIYAPATNA",
    "block": "PIRIYAPATNA",
    "village": "Piriyapatna",
    "latitude": 12.333333,
    "longitude": 76.1,
    "monitoringDate": "2024-01-05",
    "current": 16.7,
    "predicted": 19.41,
    "change": 2.71,
    "risk": "High",
    "probabilities": {
      "no": 24.0,
      "low": 18.3,
      "moderate": 27.4,
      "high": 30.3
    },
    "history": [
      {
        "date": "nan",
        "level": 7.95
      },
      {
        "date": "nan",
        "level": 10.96
      },
      {
        "date": "nan",
        "level": 8.05
      },
      {
        "date": "2022-05-11",
        "level": 8.67
      },
      {
        "date": "2023-05-01",
        "level": 11.12
      },
      {
        "date": "nan",
        "level": 13.45
      },
      {
        "date": "nan",
        "level": 12.58
      },
      {
        "date": "2024-05-01",
        "level": 16.7
      }
    ]
  },
  {
    "name": "Piriyapatna1",
    "district": "Mysore",
    "tehsil": "NANJANGUD",
    "block": "NANJANGUD",
    "village": "Piriyapatna",
    "latitude": 12.116667,
    "longitude": 76.683333,
    "monitoringDate": "2023-05-26",
    "current": 9.4,
    "predicted": 9.05,
    "change": -0.35,
    "risk": "No Depletion",
    "probabilities": {
      "no": 64.2,
      "low": 16.6,
      "moderate": 9.2,
      "high": 9.9
    },
    "history": [
      {
        "date": "nan",
        "level": 11.0
      },
      {
        "date": "2015-05-11",
        "level": 4.38
      },
      {
        "date": "nan",
        "level": 11.0
      },
      {
        "date": "nan",
        "level": 11.0
      },
      {
        "date": "2017-05-01",
        "level": 11.0
      },
      {
        "date": "nan",
        "level": 11.0
      },
      {
        "date": "2019-05-01",
        "level": 8.9
      },
      {
        "date": "nan",
        "level": 9.4
      }
    ]
  },
  {
    "name": "Punnadahalli Koppalu",
    "district": "Mysore",
    "tehsil": "PIRIYAPATNA",
    "block": "PIRIYAPATNA",
    "village": "Punnadahalli Koppalu",
    "latitude": 12.394722,
    "longitude": 76.046667,
    "monitoringDate": "2024-01-05",
    "current": 10.07,
    "predicted": 8.97,
    "change": -1.1,
    "risk": "High",
    "probabilities": {
      "no": 28.1,
      "low": 19.8,
      "moderate": 16.1,
      "high": 35.9
    },
    "history": [
      {
        "date": "nan",
        "level": 5.32
      },
      {
        "date": "nan",
        "level": 2.1
      },
      {
        "date": "2022-05-11",
        "level": 2.1
      },
      {
        "date": "2023-05-01",
        "level": 4.5
      },
      {
        "date": "nan",
        "level": 8.5
      },
      {
        "date": "nan",
        "level": 4.8
      },
      {
        "date": "2023-05-11",
        "level": 7.79
      },
      {
        "date": "2024-05-01",
        "level": 10.07
      }
    ]
  },
  {
    "name": "Ranganathapura",
    "district": "Mysore",
    "tehsil": "PIRIYAPATNA",
    "block": "PIRIYAPATNA",
    "village": "Ranganathapura",
    "latitude": 12.425,
    "longitude": 76.0,
    "monitoringDate": "2023-11-05",
    "current": 5.65,
    "predicted": 4.9,
    "change": -0.75,
    "risk": "Low",
    "probabilities": {
      "no": 21.9,
      "low": 39.6,
      "moderate": 19.1,
      "high": 19.5
    },
    "history": [
      {
        "date": "nan",
        "level": 4.55
      },
      {
        "date": "nan",
        "level": 1.07
      },
      {
        "date": "nan",
        "level": 2.5
      },
      {
        "date": "nan",
        "level": 1.8
      },
      {
        "date": "nan",
        "level": 1.95
      },
      {
        "date": "nan",
        "level": 4.45
      },
      {
        "date": "nan",
        "level": 3.05
      },
      {
        "date": "2023-05-11",
        "level": 5.65
      }
    ]
  },
  {
    "name": "Rathnapuri",
    "district": "Mysore",
    "tehsil": "HUNSUR",
    "block": "HUNSUR",
    "village": "Rathnapuri",
    "latitude": 12.238889,
    "longitude": 76.341667,
    "monitoringDate": "2024-01-05",
    "current": 3.48,
    "predicted": 5.93,
    "change": 2.45,
    "risk": "High",
    "probabilities": {
      "no": 18.1,
      "low": 17.7,
      "moderate": 31.5,
      "high": 32.7
    },
    "history": [
      {
        "date": "nan",
        "level": 1.51
      },
      {
        "date": "nan",
        "level": 0.6
      },
      {
        "date": "2022-05-11",
        "level": 0.65
      },
      {
        "date": "2023-05-01",
        "level": 2.4
      },
      {
        "date": "nan",
        "level": 4.22
      },
      {
        "date": "nan",
        "level": 6.7
      },
      {
        "date": "2023-05-11",
        "level": 2.6
      },
      {
        "date": "2024-05-01",
        "level": 3.48
      }
    ]
  },
  {
    "name": "Saligrama",
    "district": "Mysore",
    "tehsil": "KRISHNARAJANAGARA",
    "block": "KRISHNARAJANAGARA",
    "village": "Saligrama",
    "latitude": 12.55,
    "longitude": 76.25,
    "monitoringDate": "2024-01-05",
    "current": 5.9,
    "predicted": 7.46,
    "change": 1.56,
    "risk": "No Depletion",
    "probabilities": {
      "no": 30.2,
      "low": 27.1,
      "moderate": 27.9,
      "high": 14.8
    },
    "history": [
      {
        "date": "nan",
        "level": 5.62
      },
      {
        "date": "nan",
        "level": 3.1
      },
      {
        "date": "nan",
        "level": 2.53
      },
      {
        "date": "2022-05-11",
        "level": 2.0
      },
      {
        "date": "2023-05-01",
        "level": 4.9
      },
      {
        "date": "nan",
        "level": 6.45
      },
      {
        "date": "nan",
        "level": 7.28
      },
      {
        "date": "2024-05-01",
        "level": 5.9
      }
    ]
  },
  {
    "name": "Saligrama1",
    "district": "Mysore",
    "tehsil": "KRISHNARAJANAGARA",
    "block": "KRISHNARAJANAGARA",
    "village": "Saligrama",
    "latitude": 12.504167,
    "longitude": 76.291667,
    "monitoringDate": "2024-01-05",
    "current": 4.3,
    "predicted": 5.74,
    "change": 1.44,
    "risk": "Low",
    "probabilities": {
      "no": 28.0,
      "low": 35.0,
      "moderate": 21.3,
      "high": 15.7
    },
    "history": [
      {
        "date": "nan",
        "level": 3.26
      },
      {
        "date": "nan",
        "level": 0.74
      },
      {
        "date": "nan",
        "level": 2.79
      },
      {
        "date": "2022-05-11",
        "level": 2.79
      },
      {
        "date": "2023-05-01",
        "level": 4.22
      },
      {
        "date": "nan",
        "level": 3.95
      },
      {
        "date": "nan",
        "level": 3.61
      },
      {
        "date": "2024-05-01",
        "level": 4.3
      }
    ]
  },
  {
    "name": "Saragur",
    "district": "Mysore",
    "tehsil": "HEGGADADEVANKOTE",
    "block": "HEGGADADEVANKOTE",
    "village": "Saragur",
    "latitude": 12.120833,
    "longitude": 76.466667,
    "monitoringDate": "2024-01-05",
    "current": 11.03,
    "predicted": 9.67,
    "change": -1.36,
    "risk": "No Depletion",
    "probabilities": {
      "no": 32.2,
      "low": 32.0,
      "moderate": 26.3,
      "high": 9.5
    },
    "history": [
      {
        "date": "nan",
        "level": 4.71
      },
      {
        "date": "nan",
        "level": 3.36
      },
      {
        "date": "2022-05-11",
        "level": 3.66
      },
      {
        "date": "2023-05-01",
        "level": 6.7
      },
      {
        "date": "nan",
        "level": 5.75
      },
      {
        "date": "nan",
        "level": 5.25
      },
      {
        "date": "2023-05-11",
        "level": 4.7
      },
      {
        "date": "2024-05-01",
        "level": 11.03
      }
    ]
  },
  {
    "name": "Shiriyur",
    "district": "Mysore",
    "tehsil": "HUNSUR",
    "block": "HUNSUR",
    "village": "Shiriyur",
    "latitude": 12.382222,
    "longitude": 76.394167,
    "monitoringDate": "2024-01-05",
    "current": 11.5,
    "predicted": 14.54,
    "change": 3.04,
    "risk": "High",
    "probabilities": {
      "no": 23.3,
      "low": 6.9,
      "moderate": 16.8,
      "high": 52.9
    },
    "history": [
      {
        "date": "nan",
        "level": 8.7
      },
      {
        "date": "nan",
        "level": 9.3
      },
      {
        "date": "2022-05-11",
        "level": 6.85
      },
      {
        "date": "2023-05-01",
        "level": 13.95
      },
      {
        "date": "nan",
        "level": 18.92
      },
      {
        "date": "nan",
        "level": 18.15
      },
      {
        "date": "2023-05-11",
        "level": 4.78
      },
      {
        "date": "2024-05-01",
        "level": 11.5
      }
    ]
  },
  {
    "name": "Siddalingapura",
    "district": "Mysore",
    "tehsil": "MYSORE",
    "block": "MYSORE",
    "village": "Siddalingapura",
    "latitude": 12.358333,
    "longitude": 76.661111,
    "monitoringDate": "2024-01-05",
    "current": 3.4,
    "predicted": 3.88,
    "change": 0.48,
    "risk": "Low",
    "probabilities": {
      "no": 29.7,
      "low": 39.2,
      "moderate": 17.4,
      "high": 13.7
    },
    "history": [
      {
        "date": "nan",
        "level": 1.05
      },
      {
        "date": "nan",
        "level": 1.19
      },
      {
        "date": "2022-05-11",
        "level": 1.04
      },
      {
        "date": "2023-05-01",
        "level": 2.1
      },
      {
        "date": "nan",
        "level": 2.7
      },
      {
        "date": "nan",
        "level": 2.5
      },
      {
        "date": "2023-05-11",
        "level": 2.09
      },
      {
        "date": "2024-05-01",
        "level": 3.4
      }
    ]
  },
  {
    "name": "Sindhuvalli",
    "district": "Mysore",
    "tehsil": "MYSORE",
    "block": "MYSORE",
    "village": "Sindhuvalli",
    "latitude": 12.269444,
    "longitude": 76.670833,
    "monitoringDate": "2013-05-15",
    "current": 26.33,
    "predicted": 11.49,
    "change": -14.84,
    "risk": "No Depletion",
    "probabilities": {
      "no": 62.5,
      "low": 10.6,
      "moderate": 8.8,
      "high": 18.1
    },
    "history": [
      {
        "date": "2009-05-01",
        "level": 2.68
      },
      {
        "date": "nan",
        "level": 10.06
      },
      {
        "date": "nan",
        "level": 3.03
      },
      {
        "date": "2010-05-01",
        "level": 2.55
      },
      {
        "date": "nan",
        "level": 3.48
      },
      {
        "date": "2011-05-11",
        "level": 3.23
      },
      {
        "date": "2012-05-01",
        "level": 2.48
      },
      {
        "date": "nan",
        "level": 26.33
      }
    ]
  },
  {
    "name": "Somanathapura",
    "district": "Mysore",
    "tehsil": "TIRUMAKUDAL-NARSIPUR",
    "block": "TIRUMAKUDAL-NARSIPUR",
    "village": "Somanathapura",
    "latitude": 12.133333,
    "longitude": 76.941667,
    "monitoringDate": "2024-01-05",
    "current": 7.4,
    "predicted": 9.07,
    "change": 1.67,
    "risk": "High",
    "probabilities": {
      "no": 20.1,
      "low": 19.9,
      "moderate": 29.3,
      "high": 30.7
    },
    "history": [
      {
        "date": "nan",
        "level": 0.8
      },
      {
        "date": "nan",
        "level": 5.99
      },
      {
        "date": "nan",
        "level": 3.96
      },
      {
        "date": "nan",
        "level": 4.0
      },
      {
        "date": "2022-05-11",
        "level": 2.61
      },
      {
        "date": "2023-05-01",
        "level": 8.15
      },
      {
        "date": "nan",
        "level": 8.53
      },
      {
        "date": "2024-05-01",
        "level": 7.4
      }
    ]
  },
  {
    "name": "Thandavapura",
    "district": "Mysore",
    "tehsil": "NANJANGUD",
    "block": "NANJANGUD",
    "village": "Thandavapura",
    "latitude": 12.175,
    "longitude": 76.725,
    "monitoringDate": "2024-01-05",
    "current": 15.15,
    "predicted": 16.07,
    "change": 0.92,
    "risk": "No Depletion",
    "probabilities": {
      "no": 36.9,
      "low": 14.1,
      "moderate": 19.9,
      "high": 29.1
    },
    "history": [
      {
        "date": "nan",
        "level": 16.24
      },
      {
        "date": "nan",
        "level": 6.82
      },
      {
        "date": "nan",
        "level": 12.15
      },
      {
        "date": "nan",
        "level": 11.82
      },
      {
        "date": "2022-05-11",
        "level": 10.82
      },
      {
        "date": "2023-05-01",
        "level": 14.87
      },
      {
        "date": "nan",
        "level": 14.44
      },
      {
        "date": "2024-05-01",
        "level": 15.15
      }
    ]
  },
  {
    "name": "Varuna",
    "district": "Mysore",
    "tehsil": "MYSORE",
    "block": "MYSORE",
    "village": "Varuna",
    "latitude": 12.267222,
    "longitude": 76.745278,
    "monitoringDate": "2024-01-05",
    "current": 2.65,
    "predicted": 4.58,
    "change": 1.93,
    "risk": "Low",
    "probabilities": {
      "no": 18.5,
      "low": 28.6,
      "moderate": 25.6,
      "high": 27.3
    },
    "history": [
      {
        "date": "nan",
        "level": 0.96
      },
      {
        "date": "nan",
        "level": 1.77
      },
      {
        "date": "2022-05-11",
        "level": 1.65
      },
      {
        "date": "2023-05-01",
        "level": 4.5
      },
      {
        "date": "nan",
        "level": 5.8
      },
      {
        "date": "nan",
        "level": 3.9
      },
      {
        "date": "2023-05-11",
        "level": 2.68
      },
      {
        "date": "2024-05-01",
        "level": 2.65
      }
    ]
  },
  {
    "name": "Vidyapitha",
    "district": "Mysore",
    "tehsil": "NANJANGUD",
    "block": "NANJANGUD",
    "village": "Vidyapitha",
    "latitude": 12.105556,
    "longitude": 76.708333,
    "monitoringDate": "2024-01-05",
    "current": 3.9,
    "predicted": 5.05,
    "change": 1.15,
    "risk": "Moderate",
    "probabilities": {
      "no": 24.4,
      "low": 26.4,
      "moderate": 35.7,
      "high": 13.6
    },
    "history": [
      {
        "date": "nan",
        "level": 1.85
      },
      {
        "date": "nan",
        "level": 1.2
      },
      {
        "date": "2022-05-11",
        "level": 1.33
      },
      {
        "date": "2023-05-01",
        "level": 2.66
      },
      {
        "date": "nan",
        "level": 5.12
      },
      {
        "date": "nan",
        "level": 4.56
      },
      {
        "date": "2023-05-11",
        "level": 3.32
      },
      {
        "date": "2024-05-01",
        "level": 3.9
      }
    ]
  },
  {
    "name": "Yelemuddanahalli",
    "district": "Mysore",
    "tehsil": "PIRIYAPATNA",
    "block": "PIRIYAPATNA",
    "village": "Yelemuddanahalli",
    "latitude": 12.248611,
    "longitude": 76.059722,
    "monitoringDate": "2024-01-05",
    "current": 1.75,
    "predicted": 8.55,
    "change": 6.8,
    "risk": "Low",
    "probabilities": {
      "no": 17.4,
      "low": 28.4,
      "moderate": 27.4,
      "high": 26.7
    },
    "history": [
      {
        "date": "nan",
        "level": 0.43
      },
      {
        "date": "nan",
        "level": 0.78
      },
      {
        "date": "nan",
        "level": 0.38
      },
      {
        "date": "2022-05-11",
        "level": 0.43
      },
      {
        "date": "2023-05-01",
        "level": 1.35
      },
      {
        "date": "nan",
        "level": 3.1
      },
      {
        "date": "nan",
        "level": 2.9
      },
      {
        "date": "2024-05-01",
        "level": 1.75
      }
    ]
  }
];

export const REAL_FEATURES = [
  {
    "name": "groundwater_level_m",
    "score": 0.5923
  },
  {
    "name": "gw_rolling_mean_4",
    "score": 0.3276
  },
  {
    "name": "month_cos",
    "score": 0.1474
  },
  {
    "name": "station_historical_mean",
    "score": 0.1203
  },
  {
    "name": "month_sin",
    "score": 0.0286
  },
  {
    "name": "Station",
    "score": 0.0242
  },
  {
    "name": "gw_lag_4",
    "score": 0.0212
  },
  {
    "name": "station_historical_std",
    "score": 0.0207
  },
  {
    "name": "gw_lag_1",
    "score": 0.0153
  },
  {
    "name": "gw_rolling_mean_3",
    "score": 0.0153
  }
];
