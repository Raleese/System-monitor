import { useEffect, useState } from 'react';
import type { Metrics } from '../utils/interfaces';
import { getLatestMetrics, getMetricsHistory } from '../utils/api_requests';
import MetricChart from './components/MetricChart';

function App() {

    const [metrics, setMetrics] = useState<Metrics | null>(null);
    const [history, setHistory] = useState<Metrics[]>([]);

    useEffect(() => {
        let isMounted = true;

        const fetchMetrics = async () => {
            try {
                const latestMetrics = await getLatestMetrics();
                const latestHistory = await getMetricsHistory();
                if (isMounted) {
                    setMetrics(latestMetrics);
                    setHistory(latestHistory);
                }
            } catch (error) {
                console.error("Error fetching metrics:", error);
            }
        };

        fetchMetrics();

        const intervalId = window.setInterval(fetchMetrics, 10000);

        return () => {
            isMounted = false;
            window.clearInterval(intervalId);
        };
    }, []);

    if (!metrics) {
        return <div>Loading...</div>;
    }

    return (
        <div className="App">
            <div className="flex flex-col items-center justify-center gap-4 p-4">
                <h1 className="text-2xl font-bold">System Infrastructure Monitor</h1>
                <div className="w-full rounded-lg border border-slate-300 bg-slate-100 p-4 shadow-sm">
                    <div className="flex w-full flex-col items-center gap-6">
                        <p className="font-semibold text-slate-700">Machine: {metrics.hostname}</p>
                        <div className="flex w-full flex-col gap-6 md:flex-row md:items-start">
                            <div className="md:w-1/3">
                                <p>CPU Usage: {metrics.cpu}%</p>
                                <MetricChart
                                    data={history.slice(-10)} // Show only the last 10 data points
                                    metric="cpu"
                                    title="CPU Usage"
                                    color="#ef4444"
                                />
                            </div>
                            <div className="md:w-1/3">
                                <p>Memory Usage: {metrics.memory}%</p>
                                <MetricChart
                                    data={history.slice(-10)} // Show only the last 10 data points
                                    metric="memory"
                                    title="Memory Usage"
                                    color="#3b82f6"
                                />
                            </div>
                            <div className="md:w-1/3">
                                <p>Disk Usage: {metrics.disk}%</p>
                                <MetricChart
                                    data={history.slice(-10)} // Show only the last 10 data points
                                    metric="disk"
                                    title="Disk Usage"
                                    color="#8b5cf6"
                                />
                            </div>
                        </div>
                        <p>Last Updated: {new Date(metrics.timestamp).toLocaleString()}</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;