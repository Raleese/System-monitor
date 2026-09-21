import { useEffect, useState } from 'react';
import type { Metrics, Alert, Device } from '../utils/interfaces';
import { getLatestMetrics, getMetricsHistory, getAlerts, getDeviceIds } from '../utils/api_requests';
import MetricChart from './components/MetricChart';

function App() {

    const [devices, setDevices] = useState<Device[]>([]);
    const [selectedDeviceId, setSelectedDeviceId] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchDeviceIds = async () => {
            try {
                const devices = await getDeviceIds();
                setDevices(devices);
                setSelectedDeviceId((currentDeviceId) =>
                    devices.some((device) => device.device_id === currentDeviceId)
                        ? currentDeviceId
                        : devices[0]?.device_id ?? '',
                );
            } catch (error) {
                console.error("Error fetching device IDs:", error);
                setError('Unable to load monitored devices.');
            }
        };
        fetchDeviceIds();

        const intervalId = window.setInterval(fetchDeviceIds, 30000);
        return () => window.clearInterval(intervalId);
    }, []);

    const [metrics, setMetrics] = useState<Metrics | null>(null);
    const [history, setHistory] = useState<Metrics[]>([]);
    const [alerts, setAlerts] = useState<Alert[]>([]);

    useEffect(() => {
        let isMounted = true;

        const fetchMetrics = async () => {
            try {
                if (!selectedDeviceId) {
                    return;
                }
                const [latestMetrics, latestHistory, latestAlerts] = await Promise.all([
                    getLatestMetrics(selectedDeviceId),
                    getMetricsHistory(selectedDeviceId),
                    getAlerts(selectedDeviceId),
                ]);
                if (isMounted) {
                    setMetrics(latestMetrics);
                    setHistory(latestHistory);
                    setAlerts(latestAlerts);
                    setError('');
                }
            } catch (error) {
                console.error("Error fetching metrics:", error);
                if (isMounted) {
                    setError('Unable to load metrics for this device.');
                }
            }
        };

        fetchMetrics();

        const intervalId = window.setInterval(fetchMetrics, 10000);

        return () => {
            isMounted = false;
            window.clearInterval(intervalId);
        };
    }, [selectedDeviceId]);

    if (!devices.length) {
        return <div className="flex min-h-screen items-center justify-center bg-slate-950 p-6 text-slate-200">{error || 'Waiting for monitored devices...'}</div>;
    }

    const selectedDevice = devices.find((device) => device.device_id === selectedDeviceId);

    if (!metrics) {
        return <div className="flex min-h-screen items-center justify-center bg-slate-950 p-6 text-slate-200">{error || 'Loading metrics...'}</div>;
    }

    const hasAlert = (metric: Alert['metric']) =>
        alerts.some(
            (alert) =>
                alert.device_id === selectedDeviceId && alert.metric === metric,
        );

    return (
        <div className="min-h-screen bg-slate-950 text-slate-100">
            <div className="mx-auto flex max-w-7xl flex-col gap-6 p-4 sm:p-8">
                <header className="flex flex-col gap-4 border-b border-slate-800 pb-6 sm:flex-row sm:items-end sm:justify-between">
                    <div>
                        <p className="text-sm font-medium uppercase tracking-[0.2em] text-cyan-400">Operations dashboard</p>
                        <h1 className="mt-2 text-3xl font-semibold tracking-tight">System infrastructure monitor</h1>
                    </div>
                    <label className="flex min-w-60 flex-col gap-2 text-sm text-slate-400">
                        Monitored device
                        <select
                            value={selectedDeviceId}
                            onChange={(event) => {
                                setSelectedDeviceId(event.target.value);
                                setMetrics(null);
                            }}
                            className="rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-slate-100 outline-none focus:border-cyan-400"
                        >
                            {devices.map((device) => (
                                <option key={device.device_id} value={device.device_id}>
                                    {device.hostname} ({device.device_id.slice(0, 8)})
                                </option>
                            ))}
                        </select>
                    </label>
                </header>
                {error && <p className="border border-amber-500/40 bg-amber-500/10 px-4 py-3 text-sm text-amber-200">{error}</p>}
                <div className="w-full rounded-lg border border-slate-800 bg-slate-900/80 p-5 shadow-2xl shadow-black/20">
                    <div className="flex w-full flex-col items-center gap-6">
                        <div className="flex w-full items-center justify-between gap-4">
                            <div>
                                <p className="text-sm text-slate-400">Machine</p>
                                <p className="font-semibold text-slate-100">{selectedDevice?.hostname ?? metrics.hostname}</p>
                            </div>
                            <span className="rounded-full bg-emerald-400/10 px-3 py-1 text-xs font-medium text-emerald-300">Live</span>
                        </div>
                        <div className="flex w-full flex-col gap-6 md:flex-row md:items-start">
                            <div className="md:w-1/3">
                                <p className={hasAlert('CPU') ? 'text-red-600' : ''}>
                                    CPU usage: {hasAlert('CPU') ? 'Alert · ' : ''}{metrics.cpu}%
                                </p>
                                <MetricChart
                                    data={history.slice(-10)} // Show only the last 10 data points
                                    metric="cpu"
                                    color="#ef4444"
                                />
                            </div>
                            <div className="md:w-1/3">
                                <p className={hasAlert('Memory') ? 'text-red-600' : ''}>
                                    Memory usage: {hasAlert('Memory') ? 'Alert · ' : ''}{metrics.memory}%
                                </p>
                                <MetricChart
                                    data={history.slice(-10)} // Show only the last 10 data points
                                    metric="memory"
                                    color="#3b82f6"
                                />
                            </div>
                            <div className="md:w-1/3">
                                <p className={hasAlert('Disk') ? 'text-red-600' : ''}>
                                    Disk usage: {hasAlert('Disk') ? 'Alert · ' : ''}{metrics.disk}%
                                </p>
                                <MetricChart
                                    data={history.slice(-10)} // Show only the last 10 data points
                                    metric="disk"
                                    color="#8b5cf6"
                                />
                            </div>
                        </div>
                        <p className="w-full border-t border-slate-800 pt-4 text-sm text-slate-400">Last updated: {new Date(metrics.timestamp).toLocaleString()}</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;