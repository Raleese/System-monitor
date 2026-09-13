import type { Metrics, Alert } from './interfaces';

const API_URL = "http://localhost:8000";

export async function getLatestMetrics(): Promise<Metrics>{
    const response = await fetch(`${API_URL}/metrics/latest`);

    if (!response.ok) {
        throw new Error("Failed to fetch latest metrics");
    }

    return response.json();
}

export async function getMetricsHistory(): Promise<Metrics[]> {
    const response = await fetch(`${API_URL}/metrics/history`);

    if (!response.ok) {
        throw new Error("Failed to fetch metrics history");
    }

    return response.json(); 
}

export async function getAlerts(): Promise<Alert[]> {
    const response = await fetch(`${API_URL}/metrics/alerts`);

    if (!response.ok) {
        throw new Error("Failed to fetch alerts");
    }

    return response.json();
}