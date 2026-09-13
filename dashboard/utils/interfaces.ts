export interface Metrics {
    id: number;
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