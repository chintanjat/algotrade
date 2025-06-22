import React, { useState } from 'react';
import { Card, Switch, Select, Space, Tag, Typography, Divider, InputNumber, Button, message } from 'antd';
import { SettingOutlined, PlayCircleOutlined, PauseCircleOutlined, SaveOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;
const { Option } = Select;

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

interface StrategyDetailsPanelProps {
  strategies: Strategy[];
  onToggleStrategy: (strategyId: string, enabled: boolean) => void;
  onUpdateSignalSource: (strategyId: string, signalSource: string) => void;
  onUpdateCapitalAllocation: (strategyId: string, capital: number) => void;
}

const StrategyDetailsPanel: React.FC<StrategyDetailsPanelProps> = ({
  strategies,
  onToggleStrategy,
  onUpdateSignalSource,
  onUpdateCapitalAllocation,
}) => {
  const [editingCapital, setEditingCapital] = useState<Record<string, number>>({});
  const [savingCapital, setSavingCapital] = useState<Record<string, boolean>>({});

  const signalSources = [
    { value: 'manual', label: 'Manual' },
    { value: 'tradingview', label: 'TradingView' },
    { value: 'custom_indicator', label: 'Custom Indicator' },
    { value: 'webhook', label: 'Webhook' },
  ];

  const getStatusColor = (enabled: boolean) => {
    return enabled ? 'success' : 'default';
  };

  const getStatusText = (enabled: boolean) => {
    return enabled ? 'Active' : 'Inactive';
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const handleCapitalEdit = (strategyId: string, currentCapital: number) => {
    setEditingCapital(prev => ({ ...prev, [strategyId]: currentCapital }));
  };

  const handleCapitalSave = async (strategyId: string) => {
    const newCapital = editingCapital[strategyId];
    if (!newCapital || newCapital <= 0) {
      message.error('Please enter a valid capital amount');
      return;
    }

    setSavingCapital(prev => ({ ...prev, [strategyId]: true }));
    
    try {
      await onUpdateCapitalAllocation(strategyId, newCapital);
      message.success('Capital allocation updated successfully');
      setEditingCapital(prev => {
        const newState = { ...prev };
        delete newState[strategyId];
        return newState;
      });
    } catch (error) {
      message.error('Failed to update capital allocation');
    } finally {
      setSavingCapital(prev => ({ ...prev, [strategyId]: false }));
    }
  };

  const handleCapitalCancel = (strategyId: string) => {
    setEditingCapital(prev => {
      const newState = { ...prev };
      delete newState[strategyId];
      return newState;
    });
  };

  return (
    <Card
      title={
        <div className="flex items-center space-x-2">
          <SettingOutlined />
          <span>Trading Strategies</span>
        </div>
      }
      className="h-full"
    >
      <div className="space-y-4">
        {strategies.map((strategy) => (
          <div key={strategy.id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
            <div className="flex items-center justify-between mb-3">
              <div>
                <Title level={5} className="!mb-1">
                  {strategy.name}
                </Title>
                <Text className="text-sm text-gray-500 dark:text-gray-400">
                  {strategy.description}
                </Text>
              </div>
              <Space>
                <Tag color={getStatusColor(strategy.enabled)}>
                  {getStatusText(strategy.enabled)}
                </Tag>
                <Switch
                  checked={strategy.enabled}
                  onChange={(checked) => onToggleStrategy(strategy.id, checked)}
                  checkedChildren={<PlayCircleOutlined />}
                  unCheckedChildren={<PauseCircleOutlined />}
                />
              </Space>
            </div>

            <Divider className="my-3" />

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Text className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  Signal Source
                </Text>
                <Select
                  value={strategy.signalSource}
                  onChange={(value) => onUpdateSignalSource(strategy.id, value)}
                  className="w-full mt-1"
                  disabled={!strategy.enabled}
                >
                  {signalSources.map((source) => (
                    <Option key={source.value} value={source.value}>
                      {source.label}
                    </Option>
                  ))}
                </Select>
              </div>

              <div>
                <Text className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  Capital Allocation
                </Text>
                <div className="flex items-center space-x-2 mt-1">
                  {editingCapital[strategy.id] !== undefined ? (
                    <>
                      <InputNumber
                        value={editingCapital[strategy.id]}
                        onChange={(value) => setEditingCapital(prev => ({ 
                          ...prev, 
                          [strategy.id]: value || 0 
                        }))}
                        formatter={(value) => `₹ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                        parser={(value) => Number(value!.replace(/₹\s?|(,*)/g, ''))}
                        min={1000}
                        max={1000000}
                        step={1000}
                        className="flex-1"
                        disabled={savingCapital[strategy.id]}
                      />
                      <Button
                        type="primary"
                        size="small"
                        icon={<SaveOutlined />}
                        onClick={() => handleCapitalSave(strategy.id)}
                        loading={savingCapital[strategy.id]}
                      >
                        Save
                      </Button>
                      <Button
                        size="small"
                        onClick={() => handleCapitalCancel(strategy.id)}
                        disabled={savingCapital[strategy.id]}
                      >
                        Cancel
                      </Button>
                    </>
                  ) : (
                    <>
                      <Text className="text-lg font-semibold text-green-600 dark:text-green-400">
                        {formatCurrency(strategy.capitalAllocation)}
                      </Text>
                      <Button
                        type="link"
                        size="small"
                        onClick={() => handleCapitalEdit(strategy.id, strategy.capitalAllocation)}
                        disabled={!strategy.enabled}
                      >
                        Edit
                      </Button>
                    </>
                  )}
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
              <div>
                <Text className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  Symbols
                </Text>
                <div className="flex flex-wrap gap-1 mt-1">
                  {strategy.symbols.map((symbol) => (
                    <Tag key={symbol} color="blue">
                      {symbol}
                    </Tag>
                  ))}
                </div>
              </div>
            </div>

            {Object.keys(strategy.parameters).length > 0 && (
              <>
                <Divider className="my-3" />
                <div>
                  <Text className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    Parameters
                  </Text>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mt-1">
                    {Object.entries(strategy.parameters).map(([key, value]) => (
                      <div key={key} className="text-xs">
                        <Text className="text-gray-500 dark:text-gray-400">{key}:</Text>
                        <Text className="ml-1 font-mono">{value}</Text>
                      </div>
                    ))}
                  </div>
                </div>
              </>
            )}
          </div>
        ))}

        {strategies.length === 0 && (
          <div className="text-center py-8">
            <SettingOutlined className="text-4xl text-gray-400 mb-4" />
            <Text className="text-gray-500 dark:text-gray-400">
              No strategies configured
            </Text>
          </div>
        )}
      </div>
    </Card>
  );
};

export default StrategyDetailsPanel; 