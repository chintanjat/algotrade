import React from 'react';
import { Card } from 'antd';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const PnLPerformanceChart: React.FC = () => {
  // Mock data - in real app, this would come from API
  const data = [
    { date: '2024-01-01', pnl: 0 },
    { date: '2024-01-02', pnl: 150 },
    { date: '2024-01-03', pnl: -50 },
    { date: '2024-01-04', pnl: 300 },
    { date: '2024-01-05', pnl: 450 },
    { date: '2024-01-06', pnl: 200 },
    { date: '2024-01-07', pnl: 600 },
    { date: '2024-01-08', pnl: 800 },
    { date: '2024-01-09', pnl: 650 },
    { date: '2024-01-10', pnl: 900 },
    { date: '2024-01-11', pnl: 1200 },
    { date: '2024-01-12', pnl: 1100 },
    { date: '2024-01-13', pnl: 1400 },
    { date: '2024-01-14', pnl: 1800 },
    { date: '2024-01-15', pnl: 25000 },
  ];

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0,
    }).format(value);
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
    });
  };

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white dark:bg-gray-800 p-3 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            {formatDate(label)}
          </p>
          <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            {formatCurrency(payload[0].value)}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <Card
      title={
        <div className="flex items-center justify-between">
          <span>P&L Performance</span>
          <div className="text-sm text-gray-500 dark:text-gray-400">
            Last 15 days
          </div>
        </div>
      }
      className="h-full"
    >
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis
              dataKey="date"
              tickFormatter={formatDate}
              stroke="#6b7280"
              fontSize={12}
            />
            <YAxis
              tickFormatter={formatCurrency}
              stroke="#6b7280"
              fontSize={12}
            />
            <Tooltip content={<CustomTooltip />} />
            <Line
              type="monotone"
              dataKey="pnl"
              stroke="#3b82f6"
              strokeWidth={2}
              dot={{ fill: '#3b82f6', strokeWidth: 2, r: 4 }}
              activeDot={{ r: 6, stroke: '#3b82f6', strokeWidth: 2 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
};

export default PnLPerformanceChart; 