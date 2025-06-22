import React, { useState } from 'react';
import { Card, Alert, Button, Typography, Space } from 'antd';
import {
  ExclamationCircleOutlined,
  CloseOutlined,
  WarningOutlined,
  InfoCircleOutlined,
  CheckCircleOutlined,
} from '@ant-design/icons';

const { Text } = Typography;

interface Error {
  id: string;
  type: 'error' | 'warning' | 'info';
  message: string;
  timestamp: string;
}

interface ErrorCenterProps {
  errors: Error[];
  onDismissError: (errorId: string) => void;
}

const ErrorCenter: React.FC<ErrorCenterProps> = ({ errors, onDismissError }) => {
  const getErrorIcon = (type: Error['type']) => {
    switch (type) {
      case 'error':
        return <ExclamationCircleOutlined className="text-danger-500" />;
      case 'warning':
        return <WarningOutlined className="text-warning-500" />;
      case 'info':
        return <InfoCircleOutlined className="text-info-500" />;
    }
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (errors.length === 0) {
    return (
      <Card title="System Status" className="h-full">
        <div className="text-center py-8">
          <CheckCircleOutlined className="text-5xl text-success-500 mb-4" />
          <Text className="text-gray-500">All systems operational</Text>
        </div>
      </Card>
    );
  }

  return (
    <Card
      title={
        <Space>
          <ExclamationCircleOutlined />
          <span>System Alerts</span>
          <span className="bg-danger-100 text-danger-800 text-xs font-medium px-2 py-1 rounded-full">
            {errors.length}
          </span>
        </Space>
      }
    >
      <div className="space-y-2">
        {errors.map((error) => (
          <Alert
            key={error.id}
            message={error.message}
            description={
              <Text type="secondary" className="text-xs">
                {formatTimestamp(error.timestamp)}
              </Text>
            }
            type={error.type}
            showIcon
            icon={getErrorIcon(error.type)}
            closable
            onClose={() => onDismissError(error.id)}
          />
        ))}
      </div>
    </Card>
  );
};

export default ErrorCenter; 