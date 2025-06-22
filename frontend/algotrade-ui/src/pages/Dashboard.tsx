import React, { useState } from 'react';
import { Row, Col, Typography } from 'antd';
import DashboardCards from '../components/DashboardCards';
import ActivePositionsTable from '../components/ActivePositionsTable';
import PnLPerformanceChart from '../components/PnLPerformanceChart';
import ErrorCenter from '../components/ErrorCenter';
import StrategyDetailsPanel from '../components/StrategyDetailsPanel';

const { Title } = Typography;

// Type definitions
interface Position {
  id: string;
  symbol: string;
  quantity: number;
  avgEntryPrice: number;
  currentPrice: number;
  marketValue: number;
  unrealizedPnL: number;
  unrealizedPnLPercent: number;
  side: 'long' | 'short';
  createdAt: string;
}

interface Error {
  id: string;
  type: 'error' | 'warning' | 'info';
  message: string;
  timestamp: string;
}

interface Strategy {
  id: string;
  name: string;
  description: string;
  enabled: boolean;
  signalSource: string;
  capitalAllocation: number;
  symbols: string[];
  parameters: Record<string, any>;
}

const Dashboard: React.FC = () => {
  // Mock data state
  const [positions, setPositions] = useState<Position[]>([
    { id: 'pos1', symbol: 'RELIANCE', quantity: 50, avgEntryPrice: 2800, currentPrice: 2850, marketValue: 142500, unrealizedPnL: 2500, unrealizedPnLPercent: 1.7, side: 'long', createdAt: '2024-01-10T09:30:00Z' },
    { id: 'pos2', symbol: 'TCS', quantity: 100, avgEntryPrice: 3800, currentPrice: 3750, marketValue: 375000, unrealizedPnL: -5000, unrealizedPnLPercent: -1.3, side: 'short', createdAt: '2024-01-12T14:00:00Z' },
  ]);

  const [systemErrors, setSystemErrors] = useState<Error[]>([
    { id: 'err1', type: 'error', message: 'Failed to connect to broker API', timestamp: new Date().toISOString() },
    { id: 'err2', type: 'warning', message: 'Market data for NIFTY is delayed', timestamp: new Date().toISOString() },
  ]);

  const [strategies, setStrategies] = useState<Strategy[]>([
    { id: 's1', name: 'MA Crossover (NIFTY 50)', description: 'Classic trend-following strategy', enabled: true, signalSource: 'manual', capitalAllocation: 50000, symbols: ['RELIANCE', 'HDFCBANK'], parameters: { fast: 10, slow: 20 } },
    { id: 's2', name: 'RSI Mean Reversion (Bank NIFTY)', description: 'Trades on overbought/oversold signals', enabled: false, signalSource: 'tradingview', capitalAllocation: 30000, symbols: ['ICICIBANK', 'SBIN'], parameters: { period: 14, overbought: 70, oversold: 30 } },
  ]);

  // Handlers
  const handleDismissError = (errorId: string) => {
    setSystemErrors(systemErrors.filter((e) => e.id !== errorId));
  };

  const handleClosePosition = (positionId: string) => {
    setPositions(positions.filter((p) => p.id !== positionId));
  };

  const handleToggleStrategy = (strategyId: string) => {
    setStrategies(
      strategies.map((s) =>
        s.id === strategyId ? { ...s, enabled: !s.enabled } : s
      )
    );
  };

  const handleUpdateSignalSource = (strategyId: string, source: string) => {
    setStrategies(
      strategies.map((s) =>
        s.id === strategyId ? { ...s, signalSource: source } : s
      )
    );
  };

  const handleUpdateCapitalAllocation = async (strategyId: string, capital: number) => {
    setStrategies(
      strategies.map((s) =>
        s.id === strategyId ? { ...s, capitalAllocation: capital } : s
      )
    );
  };

  return (
    <div className="space-y-6">
      <Title level={2}>Dashboard</Title>
      
      <DashboardCards />

      <Row gutter={[24, 24]}>
        <Col xs={24} lg={16}>
          <div className="space-y-6">
            <ActivePositionsTable
              positions={positions}
              onClosePosition={handleClosePosition}
              onViewDetails={(id) => console.log('View details for', id)}
            />
            <PnLPerformanceChart />
          </div>
        </Col>
        <Col xs={24} lg={8}>
          <div className="space-y-6">
            <StrategyDetailsPanel 
              strategies={strategies}
              onToggleStrategy={handleToggleStrategy}
              onUpdateSignalSource={handleUpdateSignalSource}
              onUpdateCapitalAllocation={handleUpdateCapitalAllocation}
            />
            <ErrorCenter errors={systemErrors} onDismissError={handleDismissError} />
          </div>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard; 