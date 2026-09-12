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
            <div className="display: flex flex-col items-center justify-center">
                <header className="App-header">
                    <h1 className="text-3xl font-bold">System Infrastructure Monitor</h1>
                    <p>Machine: {metrics.hostname}</p>
                    <p>CPU Usage: {metrics.cpu}%</p>
                    <p>Memory Usage: {metrics.memory}%</p>
                    <p>Disk Usage: {metrics.disk}%</p>
                    <p>Last Updated: {new Date(metrics.timestamp).toLocaleString()}</p>
                </header>
            </div>
        </div>
    );
}

export default App;