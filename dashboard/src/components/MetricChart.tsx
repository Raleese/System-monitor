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

function MetricChart({ data, metric, title, color }: MetricChartProps) {
    return (
        <section>
            <h2>{title}</h2>

            <ResponsiveContainer width="100%" height={300}>
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
                        type="monotone"
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