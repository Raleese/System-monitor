export interface Metrics {
    id: number;
    device_id: string;
    hostname: string;
    cpu: number;
    memory: number;
    disk: number;
    timestamp: string;
}

export interface MetricChartProps {
    data: Metrics[];
    metric: 'cpu' | 'memory' | 'disk';
    color: string;
}

export interface Alert {
    id: number;
    hostname: string;
    metric: 'CPU' | 'Memory' | 'Disk';
    value: number;
    timestamp: string;
}

export interface Device {
    device_id: string;
    hostname: string;
}