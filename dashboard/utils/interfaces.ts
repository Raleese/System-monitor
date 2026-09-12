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
    metric: 'cpu' | 'memory';
    title: string;
    color: string;
}