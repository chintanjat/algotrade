import React from 'react';
import { Typography } from 'antd';
import ActivePositionsTable from '../components/ActivePositionsTable';

const { Title } = Typography;

const Positions: React.FC = () => {
  const positions = [
    {
      id: 'pos_1',
      symbol: 'AAPL',
      quantity: 100,
      avgEntryPrice: 150.00,
      currentPrice: 155.50,
      marketValue: 15550,
      unrealizedPnL: 550,
      unrealizedPnLPercent: 3.67,
      side: 'long' as const,
      createdAt: '2024-01-15T09:30:00Z',
    },
    {
      id: 'pos_2',
      symbol: 'TSLA',
      quantity: 50,
      avgEntryPrice: 200.00,
      currentPrice: 195.00,
      marketValue: 9750,
      unrealizedPnL: -250,
      unrealizedPnLPercent: -2.5,
      side: 'long' as const,
      createdAt: '2024-01-14T14:15:00Z',
    },
  ];

  const handleClosePosition = (positionId: string) => {
    console.log('Close position:', positionId);
  };

  const handleViewDetails = (positionId: string) => {
    console.log('View position details:', positionId);
  };

  return (
    <div className="space-y-6">
      <div>
        <Title level={2} className="!mb-2">
          Active Positions
        </Title>
        <p className="text-gray-600 dark:text-gray-400">
          Monitor your current trading positions
        </p>
      </div>

      <ActivePositionsTable
        positions={positions}
        onClosePosition={handleClosePosition}
        onViewDetails={handleViewDetails}
      />
    </div>
  );
};

export default Positions; 