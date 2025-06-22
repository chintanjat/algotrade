import React, { useState } from 'react';
import { Card, Typography, Button, Space, Tag, Switch, Modal, Form, Input, Select } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, SettingOutlined } from '@ant-design/icons';

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

const Strategies: React.FC = () => {
  const [strategies, setStrategies] = useState<Strategy[]>([
    {
      id: 's1',
      name: 'MA Crossover (NIFTY 50)',
      description: 'A simple moving average crossover strategy for large-cap stocks.',
      symbols: ['RELIANCE', 'HDFCBANK', 'INFY', 'TCS'],
      signalSource: 'manual',
      enabled: true,
      capitalAllocation: 50000,
      parameters: { fast_period: 10, slow_period: 30 },
    },
    {
      id: 's2',
      name: 'RSI Mean Reversion (Bank NIFTY)',
      description: 'A mean reversion strategy based on the RSI indicator for banking stocks.',
      symbols: ['ICICIBANK', 'SBIN', 'KOTAKBANK'],
      signalSource: 'tradingview',
      enabled: false,
      capitalAllocation: 30000,
      parameters: { rsi_period: 14, oversold: 30, overbought: 70 },
    },
  ]);

  const [isModalVisible, setIsModalVisible] = useState(false);
  const [editingStrategy, setEditingStrategy] = useState<any>(null);
  const [form] = Form.useForm();

  const signalSources = [
    { value: 'manual', label: 'Manual' },
    { value: 'tradingview', label: 'TradingView' },
    { value: 'custom_indicator', label: 'Custom Indicator' },
    { value: 'webhook', label: 'Webhook' },
  ];

  const handleToggleStrategy = (strategyId: string, enabled: boolean) => {
    setStrategies(prev =>
      prev.map(strategy =>
        strategy.id === strategyId
          ? { ...strategy, enabled }
          : strategy
      )
    );
  };

  const handleCreateStrategy = () => {
    setEditingStrategy(null);
    form.resetFields();
    setIsModalVisible(true);
  };

  const handleEditStrategy = (strategy: any) => {
    setEditingStrategy(strategy);
    form.setFieldsValue(strategy);
    setIsModalVisible(true);
  };

  const handleDeleteStrategy = (strategyId: string) => {
    setStrategies(prev => prev.filter(strategy => strategy.id !== strategyId));
  };

  const handleModalOk = () => {
    form.validateFields().then((values) => {
      if (editingStrategy) {
        // Update existing strategy
        setStrategies(prev =>
          prev.map(strategy =>
            strategy.id === editingStrategy.id
              ? { ...strategy, ...values }
              : strategy
          )
        );
      } else {
        // Create new strategy
        const newStrategy = {
          id: `strategy_${Date.now()}`,
          ...values,
          enabled: false,
        };
        setStrategies(prev => [...prev, newStrategy]);
      }
      setIsModalVisible(false);
    });
  };

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

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <Title level={2} className="!mb-2">
            Trading Strategies
          </Title>
          <p className="text-gray-600 dark:text-gray-400">
            Manage your algorithmic trading strategies
          </p>
        </div>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={handleCreateStrategy}
        >
          New Strategy
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {strategies.map((strategy) => (
          <Card
            key={strategy.id}
            title={
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <SettingOutlined />
                  <span>{strategy.name}</span>
                </div>
                <Switch
                  checked={strategy.enabled}
                  onChange={(checked) => handleToggleStrategy(strategy.id, checked)}
                />
              </div>
            }
            extra={
              <Space>
                <Button
                  type="text"
                  size="small"
                  icon={<EditOutlined />}
                  onClick={() => handleEditStrategy(strategy)}
                />
                <Button
                  type="text"
                  size="small"
                  danger
                  icon={<DeleteOutlined />}
                  onClick={() => handleDeleteStrategy(strategy.id)}
                />
              </Space>
            }
            className="h-full"
          >
            <div className="space-y-4">
              <div>
                <Text className="text-gray-600 dark:text-gray-400">
                  {strategy.description}
                </Text>
              </div>

              <div className="flex items-center justify-between">
                <Tag color={getStatusColor(strategy.enabled)}>
                  {getStatusText(strategy.enabled)}
                </Tag>
                <Text className="text-sm text-gray-500 dark:text-gray-400">
                  {strategy.signalSource}
                </Text>
              </div>

              <div className="bg-gray-50 dark:bg-gray-800 p-3 rounded-lg">
                <Text className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  Capital Allocation
                </Text>
                <div className="text-lg font-semibold text-green-600 dark:text-green-400 mt-1">
                  {formatCurrency(strategy.capitalAllocation)}
                </div>
              </div>

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

              {Object.keys(strategy.parameters).length > 0 && (
                <div>
                  <Text className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    Parameters
                  </Text>
                  <div className="grid grid-cols-2 gap-2 mt-1">
                    {Object.entries(strategy.parameters).map(([key, value]) => (
                      <div key={key} className="text-xs">
                        <Text className="text-gray-500 dark:text-gray-400">{key}:</Text>
                        <Text className="ml-1 font-mono">{value}</Text>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </Card>
        ))}
      </div>

      <Modal
        title={editingStrategy ? 'Edit Strategy' : 'New Strategy'}
        open={isModalVisible}
        onOk={handleModalOk}
        onCancel={() => setIsModalVisible(false)}
        width={600}
      >
        <Form
          form={form}
          layout="vertical"
          initialValues={{
            signalSource: 'manual',
            symbols: [],
            parameters: {},
          }}
        >
          <Form.Item
            name="name"
            label="Strategy Name"
            rules={[{ required: true, message: 'Please enter strategy name' }]}
          >
            <Input placeholder="Enter strategy name" />
          </Form.Item>

          <Form.Item
            name="description"
            label="Description"
            rules={[{ required: true, message: 'Please enter description' }]}
          >
            <Input.TextArea rows={3} placeholder="Enter strategy description" />
          </Form.Item>

          <Form.Item
            name="signalSource"
            label="Signal Source"
            rules={[{ required: true, message: 'Please select signal source' }]}
          >
            <Select placeholder="Select signal source">
              {signalSources.map((source) => (
                <Option key={source.value} value={source.value}>
                  {source.label}
                </Option>
              ))}
            </Select>
          </Form.Item>

          <Form.Item
            name="symbols"
            label="Trading Symbols"
            rules={[{ required: true, message: 'Please enter trading symbols' }]}
          >
            <Select
              mode="tags"
              placeholder="Enter trading symbols"
              style={{ width: '100%' }}
            />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Strategies; 