import type { Metrics, Alert, Device } from './interfaces';

const API_URL = "http://192.168.0.4:8000";

export async function getLatestMetrics(device_id: string): Promise<Metrics>{
    const response = await fetch(`${API_URL}/metrics/latest?device_id=${device_id}`);

    if (!response.ok) {
        throw new Error("Failed to fetch latest metrics");
    }

    return response.json();
}

export async function getMetricsHistory(device_id: string): Promise<Metrics[]> {
    const response = await fetch(`${API_URL}/metrics/history?device_id=${device_id}`);

    if (!response.ok) {
        throw new Error("Failed to fetch metrics history");
    }

    return response.json(); 
}

export async function getAlerts(device_id: string): Promise<Alert[]> {
    const response = await fetch(`${API_URL}/metrics/alerts?device_id=${device_id}`);

    if (!response.ok) {
        throw new Error("Failed to fetch alerts");
    }

    return response.json();
}

export async function getDeviceIds(): Promise<Device[]> {
    const response = await fetch(`${API_URL}/metrics/devices`);

    if (!response.ok) {
        throw new Error("Failed to fetch device IDs");
    }

    return response.json();
}