import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer
} from "recharts";
import type { MetricChartProps } from "../../utils/interfaces";

function MetricChart({ data, metric, color }: MetricChartProps) {
    return (
        <section>
            <ResponsiveContainer width="100%" height={200}>
                <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                        dataKey="timestamp"
                        tickFormatter={(timestamp) =>
                            new Date(timestamp).toLocaleTimeString()
                        }
                    />
                    <YAxis domain={[0, 100]} />
                    <Tooltip />
                    <Line
                        dataKey={metric}
                        stroke={color}
                        strokeWidth={2}
                        dot={false}
                    />
                </LineChart>
            </ResponsiveContainer>
        </section>
    );
}

export default MetricChart;