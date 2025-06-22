import React from 'react';
import { Table, Card, Tag, Button, Space, Typography } from 'antd';
import { CloseOutlined, EyeOutlined } from '@ant-design/icons';

const { Text } = Typography;

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

interface ActivePositionsTableProps {
  positions: Position[];
  onClosePosition: (positionId: string) => void;
  onViewDetails: (positionId: string) => void;
}

const ActivePositionsTable: React.FC<ActivePositionsTableProps> = ({
  positions,
  onClosePosition,
  onViewDetails,
}) => {
  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
    }).format(amount);
  };

  const formatPercentage = (value: number) => {
    return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`;
  };

  const getPnLColor = (value: number) => {
    return value >= 0 ? 'text-success-600 dark:text-success-400' : 'text-danger-600 dark:text-danger-400';
  };

  const getSideColor = (side: string) => {
    return side === 'long' ? 'green' : 'red';
  };

  const columns = [
    {
      title: 'Symbol',
      dataIndex: 'symbol',
      key: 'symbol',
      render: (symbol: string) => (
        <Text className="font-semibold text-gray-900 dark:text-gray-100">
          {symbol}
        </Text>
      ),
    },
    {
      title: 'Side',
      dataIndex: 'side',
      key: 'side',
      render: (side: string) => (
        <Tag color={getSideColor(side)} className="capitalize">
          {side}
        </Tag>
      ),
    },
    {
      title: 'Quantity',
      dataIndex: 'quantity',
      key: 'quantity',
      render: (quantity: number) => (
        <Text className="font-mono">{quantity.toLocaleString()}</Text>
      ),
    },
    {
      title: 'Avg Entry',
      dataIndex: 'avgEntryPrice',
      key: 'avgEntryPrice',
      render: (price: number) => (
        <Text className="font-mono">{formatCurrency(price)}</Text>
      ),
    },
    {
      title: 'Current Price',
      dataIndex: 'currentPrice',
      key: 'currentPrice',
      render: (price: number) => (
        <Text className="font-mono font-semibold">{formatCurrency(price)}</Text>
      ),
    },
    {
      title: 'Market Value',
      dataIndex: 'marketValue',
      key: 'marketValue',
      render: (value: number) => (
        <Text className="font-mono">{formatCurrency(value)}</Text>
      ),
    },
    {
      title: 'Unrealized P&L',
      dataIndex: 'unrealizedPnL',
      key: 'unrealizedPnL',
      render: (pnl: number, record: Position) => (
        <div>
          <div className={`font-mono font-semibold ${getPnLColor(pnl)}`}>
            {formatCurrency(pnl)}
          </div>
          <div className={`text-xs ${getPnLColor(record.unrealizedPnLPercent)}`}>
            {formatPercentage(record.unrealizedPnLPercent)}
          </div>
        </div>
      ),
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: Position) => (
        <Space>
          <Button
            type="text"
            size="small"
            icon={<EyeOutlined />}
            onClick={() => onViewDetails(record.id)}
          />
          <Button
            type="text"
            size="small"
            danger
            icon={<CloseOutlined />}
            onClick={() => onClosePosition(record.id)}
          />
        </Space>
      ),
    },
  ];

  return (
    <Card
      title={
        <div className="flex items-center justify-between">
          <span>Active Positions</span>
          <Text className="text-sm text-gray-500 dark:text-gray-400">
            {positions.length} position{positions.length !== 1 ? 's' : ''}
          </Text>
        </div>
      }
      className="h-full"
    >
      <Table
        columns={columns}
        dataSource={positions}
        rowKey="id"
        pagination={false}
        size="small"
        scroll={{ x: 800 }}
        locale={{
          emptyText: (
            <div className="py-8 text-center">
              <Text className="text-gray-500 dark:text-gray-400">
                No active positions
              </Text>
            </div>
          ),
        }}
      />
    </Card>
  );
};

export default ActivePositionsTable; 